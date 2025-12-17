import boto3
import zipfile
import os


LAMBDA_FUNCTION_NAME = 'MyResumeViewsCountFunction'  
REGION = 'us-east-1'  

def create_deployment_package():
    """Zip up the Lambda function"""
    zip_file = 'lambda_deployment.zip'
    
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write('lambda_function.py', 'lambda_function.py')
    
    print(f"✓ Created {zip_file}")
    return zip_file

def deploy_lambda(zip_file):
    """Upload to AWS Lambda"""
    lambda_client = boto3.client('lambda', region_name=REGION)
    
    with open(zip_file, 'rb') as f:
        zip_content = f.read()
    
    response = lambda_client.update_function_code(
        FunctionName=LAMBDA_FUNCTION_NAME,
        ZipFile=zip_content
    )
    
    print(f"✓ Deployed to Lambda: {response['FunctionName']}")
    print(f"✓ Version: {response['Version']}")

if __name__ == '__main__':
    print("Starting deployment...")
    zip_file = create_deployment_package()
    deploy_lambda(zip_file)
    
    # Clean up
    os.remove(zip_file)
    print("✓ Deployment complete!")