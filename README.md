# Kubernetes-DevSecOps-CI-CD-Project

### Project Introduction:
Welcome to the End-to-End DevSecOps Kubernetes Project guide! In this comprehensive project, we will walk through the process of setting up a robust Three-Tier architecture on AWS using Kubernetes, DevOps best practices, and security measures. This project aims to provide hands-on experience in deploying, securing, and monitoring a scalable application environment.

### Project Overview:
In this project, we will cover the following key aspects:

1. IAM User Setup: Create an IAM user on AWS with the necessary permissions to facilitate deployment and management activities.
2. Infrastructure as Code (IaC): Use Terraform and AWS CLI to set up the Jenkins server (EC2 instance) on AWS.
3. Jenkins Server Configuration: Install and configure essential tools on the Jenkins server, including Jenkins itself, Docker, Sonarqube, Terraform, Kubectl, AWS CLI, and Trivy.
4. EKS Cluster Deployment: Utilize eksctl commands to create an Amazon EKS cluster, a managed Kubernetes service on AWS.
5. Load Balancer Configuration: Configure AWS Application Load Balancer (ALB) for the EKS cluster.
6. Amazon ECR Repositories: Create private repositories for both frontend and backend Docker images on Amazon Elastic Container Registry (ECR).
7. ArgoCD Installation: Install and set up ArgoCD for continuous delivery and GitOps.
8. Sonarqube Integration: Integrate Sonarqube for code quality analysis in the DevSecOps pipeline.
9. Jenkins Pipelines: Create Jenkins pipelines for deploying backend and frontend code to the EKS cluster.
10. Monitoring Setup: Implement monitoring for the EKS cluster using Helm, Prometheus, and Grafana.
11. ArgoCD Application Deployment: Use ArgoCD to deploy the Three-Tier application, including database, backend, frontend, and ingress components.
12. DNS Configuration: Configure DNS settings to make the application accessible via custom subdomains.
13. Data Persistence: Implement persistent volume and persistent volume claims for database pods to ensure data persistence.
14. Conclusion and Monitoring: Conclude the project by summarizing key achievements and monitoring the EKS cluster’s performance using Grafana.

### Prerequisites:
Before starting the project, ensure you have the following prerequisites:

- An AWS account with the necessary permissions to create resources.
- Terraform and AWS CLI installed on your local machine.
- Basic familiarity with Kubernetes, Docker, Jenkins, and DevOps principles.

### Step 1: Create an IAM user and generate the AWS Access key
Create a new IAM User on AWS and give it to the AdministratorAccess for testing purposes (not recommended for your Organization's Projects)
Go to the AWS IAM Service and click on Users.
[image]
Click on Create user

[image]
Provide the name to your user and click on Next.

[image]
Select the Attach policies directly option and search for AdministratorAccess then select it.

Click on the Next.

[image]
Click on Create user

[image]
Now, Select your created user then click on Security credentials and generate access key by clicking on Create access key.
[image]

Select the Command Line Interface (CLI) then select the checkmark for the confirmation and click on Next.
[image]

Provide the Description and click on the Create access key.
[image]

Here, you will see that you got the credentials and also you can download the CSV file for the future.
[image]

### Step 2: Install Terraform & AWS CLI to deploy our Jenkins Server(EC2) on AWS.
Install & Configure Terraform and AWS CLI on your local machine to create Jenkins Server on AWS Cloud

#### Terraform Installation Script 
```
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg - dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update
sudo apt install terraform -y
```

#### AWSCLI Installation Script
```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip -y
unzip awscliv2.zip
sudo ./aws/install
```
Now, Configure both the tools

#### Configure Terraform

Edit the file /etc/environment using the below command add the highlighted lines and add your keys in the blur space.

`sudo vim /etc/environment`
[image]

After doing the changes, restart your machine to reflect the changes of your environment variables.

#### Configure AWS CLI

Run the below command, and add your keys

`aws configure`
[image]

### Step 3: 

### Step 4: 

### Step 5: 

### Step 6: 

### Step 7: 

### Step 8: 

### Step 9: 

### Step 10: 

### Step 11: 

### Conclusion: 
