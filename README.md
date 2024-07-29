# iris-flask-aws-webapp

## Description

This repository contains an example web application built with Flask for classifying iris flower species. 

- **GitHub** is used for version control of the project files.
- **AWS** (Amazon Web Services) is used to deploy and manage the web application.
- **SageMaker** is used for training and deploying machine learning models.
- **GitHub Actions** is set up for continuous integration and continuous deployment (CI/CD).

## Steps to Set Up

### 1. **Set Up AWS Environment**

- [ ] **Create an AWS Account**
  - Sign up for a free AWS account if you don't already have one.

- [ ] **Install AWS CLI**
  - Install and configure the AWS Command Line Interface (CLI) on your local machine.

- [ ] **Create IAM Role**
  - Go to the IAM Console.
  - Create a new role with the following permissions:
    - `AmazonSageMakerFullAccess`
    - `AmazonS3FullAccess`

- [ ] **Create S3 Bucket**
  - Go to the S3 Console.
  - Create a new bucket (e.g., `iris-flask-webapp-bucket`).

### 2. **Prepare the Environment**

- [ ] **Set Up SageMaker Notebook Instance**
  - Open the SageMaker Console.
  - Create a new notebook instance.
  - Attach the IAM role created earlier.
  - Open the notebook once it's running.

- [ ] **Clone GitHub Repository in SageMaker Notebook**
  - Open a terminal in the SageMaker notebook instance.
  - Clone the repository:

    ```bash
    git clone https://github.com/marcusRB/iris-flask-webapp.git
    cd iris-flask-webapp
    ```

- [ ] **Create Python Environment and Install Requirements**
  - In the terminal of your SageMaker notebook, create a virtual environment:

    ```bash
    python -m venv env
    source env/bin/activate
    ```

  - Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

### 3. **Train the Model**

- [ ] **Prepare Training Script**
  - Ensure the `train.py` script is available in the cloned repository.

- [ ] **Create and Run Training Job**
  - In the SageMaker notebook, use the following script to train the model:

    ```python
    import sagemaker
    from sagemaker.sklearn.estimator import SKLearn

    sagemaker_session = sagemaker.Session()
    role = 'Your-SageMaker-Execution-Role-ARN'

    sklearn = SKLearn(entry_point='train.py',
                      role=role,
                      instance_type='ml.t2.medium',
                      sagemaker_session=sagemaker_session)

    sklearn.fit()
    ```

### 4. **Deploy the Model**

- [ ] **Deploy the Model**
  - Use the SageMaker SDK to deploy the model:

    ```python
    predictor = sklearn.deploy(instance_type='ml.t2.medium', initial_instance_count=1)
    ```

- [ ] **Test the Endpoint**
  - Use the deployed endpoint for inference:

    ```python
    response = predictor.predict([your_test_data])
    print(response)
    ```

### 5. **Set Up CI/CD with GitHub Actions**

- [ ] **Create GitHub Actions Workflow**
  - In the `iris-flask-webapp` repository, create a `.github/workflows` directory.
  - Add a new workflow file (e.g., `deploy.yml`) with the following content:

    ```yaml
    name: Deploy to SageMaker

    on:
      push:
        branches:
          - main

    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
          - name: Checkout code
            uses: actions/checkout@v2
          
          - name: Configure AWS credentials
            uses: aws-actions/configure-aws-credentials@v1
            with:
              aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
              aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
              aws-region: us-east-1
          
          - name: Create Training Job
            run: |
              aws sagemaker create-training-job --cli-input-json file://config/training-config.json
          
          - name: Deploy Model
            run: |
              aws sagemaker create-endpoint --cli-input-json file://config/endpoint-config.json
    ```

- [ ] **Add AWS Credentials**
  - Go to your GitHub repository settings.
  - Add `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` as secrets.

### 6. **Testing and Validation**

- [ ] **Test the Model Endpoint**
  - Validate the deployed model by sending requests and checking responses.

## Additional Notes

- Ensure that you are using the free tier services to avoid unexpected charges.
- Keep an eye on the AWS billing dashboard to monitor usage.

Feel free to contribute to the repository and make improvements!
