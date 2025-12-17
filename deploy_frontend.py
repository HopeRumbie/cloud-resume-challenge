import boto3
import os
import mimetypes

S3_BUCKET = 'hopemupupuni'
CLOUDFRONT_DISTRIBUTION_ID = 'E2UUAEJMD82E27'
REGION = 'us-east-1'

def upload_to_s3():
    """Upload frontend files to S3"""
    s3_client = boto3.client('s3', region_name=REGION)
    frontend_dir = 'frontend'
    files_uploaded = 0
    
    # Only walk through frontend directory
    for root, dirs, files in os.walk(frontend_dir):
        for file in files:
            # Full path to file
            local_path = os.path.join(root, file)
            
            # S3 key should be relative path WITHOUT 'frontend/' prefix
            relative_path = os.path.relpath(local_path, frontend_dir)
            s3_key = relative_path.replace('\\', '/')
            
            # Determine content type
            content_type, _ = mimetypes.guess_type(local_path)
            if content_type is None:
                content_type = 'application/octet-stream'
            
            extra_args = {'ContentType': content_type}
            
            # Set cache control
            if local_path.endswith('.html'):
                extra_args['CacheControl'] = 'max-age=300'
            else:
                extra_args['CacheControl'] = 'max-age=86400'
            
            s3_client.upload_file(local_path, S3_BUCKET, s3_key, ExtraArgs=extra_args)
            print(f"✓ Uploaded: {s3_key}")
            files_uploaded += 1
    
    print(f"\n✓ Uploaded {files_uploaded} files to S3")

def invalidate_cloudfront():
    """Invalidate CloudFront cache"""
    if not CLOUDFRONT_DISTRIBUTION_ID:
        print("\n⚠ Skipping CloudFront invalidation (no distribution ID configured)")
        return
    
    cloudfront_client = boto3.client('cloudfront')
    
    import time
    caller_reference = str(int(time.time()))
    
    response = cloudfront_client.create_invalidation(
        DistributionId=CLOUDFRONT_DISTRIBUTION_ID,
        InvalidationBatch={
            'Paths': {
                'Quantity': 1,
                'Items': ['/*']
            },
            'CallerReference': caller_reference
        }
    )
    
    print(f"✓ CloudFront invalidation created: {response['Invalidation']['Id']}")

if __name__ == '__main__':
    print("Starting frontend deployment...")
    upload_to_s3()
    invalidate_cloudfront()
    print("\n✓ Frontend deployment complete!")