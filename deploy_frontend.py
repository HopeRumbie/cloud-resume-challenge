import boto3
import os
import mimetypes


S3_BUCKET = 'hopemupupuni'  
CLOUDFRONT_DISTRIBUTION_ID = 'E2UUAEJMD82E27'  
REGION = 'us-east-1'
FRONTEND_DIR = 'frontend'

def upload_to_s3():
    """Upload all files to S3"""
    s3_client = boto3.client('s3', region_name=REGION)
    
    files_to_upload = []
    
    # Get all files in current directory
    for root, dirs, files in os.walk('.'):
        # Skip hidden folders and git
        if '/.git' in root or '/__pycache__' in root:
            continue
            
        for file in files:
            # Skip the deploy script itself
            if file == 'deploy_frontend.py' or file == '.gitignore':
                continue
                
            filepath = os.path.join(root, file)
            # Remove leading './' from path
            s3_key = filepath[2:] if filepath.startswith('./') else filepath
            files_to_upload.append((filepath, s3_key))
    
    # Upload each file
    for filepath, s3_key in files_to_upload:
        # Determine content type
        content_type, _ = mimetypes.guess_type(filepath)
        if content_type is None:
            content_type = 'application/octet-stream'
        
        extra_args = {'ContentType': content_type}
        
        # Set cache control for HTML files
        if filepath.endswith('.html'):
            extra_args['CacheControl'] = 'max-age=300'  # 5 minutes
        else:
            extra_args['CacheControl'] = 'max-age=86400'  # 1 day for CSS/JS/images
        
        s3_client.upload_file(filepath, S3_BUCKET, s3_key, ExtraArgs=extra_args)
        print(f"✓ Uploaded: {s3_key}")
    
    print(f"\n✓ Uploaded {len(files_to_upload)} files to S3")

def invalidate_cloudfront():
    """Invalidate CloudFront cache"""
    if not CLOUDFRONT_DISTRIBUTION_ID or CLOUDFRONT_DISTRIBUTION_ID == 'E2UUAEJMD82E27':
        print("\n⚠ Skipping CloudFront invalidation (no distribution ID configured)")
        return
    
    cloudfront_client = boto3.client('cloudfront')
    
    response = cloudfront_client.create_invalidation(
        DistributionId=CLOUDFRONT_DISTRIBUTION_ID,
        InvalidationBatch={
            'Paths': {
                'Quantity': 1,
                'Items': ['/*']
            },
            'CallerReference': str(hash(os.times()))
        }
    )
    
    print(f"✓ CloudFront invalidation created: {response['Invalidation']['Id']}")

if __name__ == '__main__':
    print("Starting frontend deployment...")
    upload_to_s3()
    invalidate_cloudfront()
    print("\n✓ Frontend deployment complete!")