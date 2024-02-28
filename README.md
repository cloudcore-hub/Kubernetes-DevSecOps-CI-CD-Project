# Kubernetes-DevSecOps-CI-CD-Project

- [Step 1: Create an IAM user and generate the AWS Access key](#step-1-create-an-iam-user-and-generate-the-aws-access-key)
- [Step 2: Install Terraform & AWS CLI to deploy our Jenkins Server(EC2) on AWS](#step-2-install-terraform--aws-cli-to-deploy-our-jenkins-server-ec2-on-aws)
- [Step 3: Deploy the Jenkins Server(EC2) using Terraform](#step-3-deploy-the-jenkins-server-ec2-using-terraform)
- [Step 4: Configure the Jenkins](#step-4-configure-the-jenkins)
- [Step 5: Deploy the EKS Cluster using eksctl commands](#step-5-deploy-the-eks-cluster-using-eksctl-commands)
- [Step 6: Configure the Load Balancer on our EKS because our application will have an ingress controller](#step-6-configure-the-load-balancer-on-our-eks-because-our-application-will-have-an-ingress-controller)
- [Step 7: Create Amazon ECR Private Repositories for both Tiers (Frontend & Backend)](#step-7-create-amazon-ecr-private-repositories-for-both-tiers-frontend--backend)
- [Step 8: Install & Configure ArgoCD](#step-8-install--configure-argocd)
- [Step 9: Configure Sonarqube for our DevSecOps Pipeline](#step-9-configure-sonarqube-for-our-devsecops-pipeline)
- [Step 10: Install the required plugins and configure the plugins to deploy our Three-Tier Application](#step-10-install-the-required-plugins-and-configure-the-plugins-to-deploy-our-three-tier-application)
- [Step 11: Set up the Monitoring for our EKS Cluster. We can monitor the Cluster Specifications and other necessary things](#step-11-set-up-the-monitoring-for-our-eks-cluster-we-can-monitor-the-cluster-specifications-and-other-necessary-things)
- [Step 12: Deploy Three-Tier Application using ArgoCD](#step-12-deploy-three-tier-application-using-argocd)
- [Conclusion](#conclusion)


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
- Basic familiarity with Kubernetes, Docker, Github Actions, Terraform, and DevOps principles.

### Step 1: SSH Exchange between local computer and Github account
`cd` to home dir and create .ssh/ folder if it doesn't exist 

```
cd ~/.ssh
ssh-keygen
```
Give the key a name `key`. List `ls` the content of .ssh/ folder.
Copy the content of the public key
```
cat key.pub
```

Go to the Settings of your Github account from profile section.
Go to Access Section on the left `SSH and GPG Keys` and `New SSH key`. Give a title and paste the content of key.pub

Back to the computer terminal and run the command
```
export GIT_SSH_COMMAND="ssh -i ~/.ssh/key"
```
Create a project folder in your `Desktop` or anywhere you'd prefer

```
mkdir ~/Desktop/project && cd ~/Desktop/project
```
#### Git Clone the application code and IaC repositories 
```
git clone https://github.com/cloudcore-hub/Kubernetes-DevSecOps-CI-CD-Project.git
git clone https://github.com/cloudcore-hub/iac_code.git
```
```
cd iac_code
git config core.sshCommand "ssh -i ~/.ssh/key -F /dev/null"
```
```
cd ..
cd Kubernetes-DevSecOps-CI-CD-Project
git config core.sshCommand "ssh -i ~/.ssh/key -F /dev/null"
```
#### Connect the repository to your Github

1. **Create a New Repository on GitHub:**
   - Go to GitHub and sign in.
   - Go to your profile and open Your repositories
   - Click the `New` icon in the top-right corner to create new repository.
   - Name your repository `iac_code`, set it to public or private, and click "Create repository."

2. **Change the Remote URL of Your Local Repository:**
   - Open your terminal and navigate to the root directory of your local repository.
   - Check the current remote URL with:
     ```
     cd iac_code
     git remote -v
     ```
   - Change the remote URL to your newly created repository with:
     ```
     git remote set-url origin <YOUR_NEW_REPOSITORY_URL>
     ```
     Replace `YOUR_NEW_REPOSITORY_URL` with the URL of your new GitHub repository, like `https://github.com/yourusername/yourrepositoryname.git`.

3. **Push Your Code to the New Repository:**
   - Ensure all your changes are committed. If you have uncommitted changes, add them using:
     ```
     git add .
     ```
   - Commit the changes with:
     ```
     git commit -m "Initial commit"
     ```
   - Push the code to your new repository with:
     ```
     git push -u origin master
     ```
     If your main branch is named differently (e.g., `main`), replace `master` with the correct branch name.

4. **Verify the Push:**
   - Refresh the GitHub page of your repository to see if the code has been pushed successfully.

5. **Repeat for the second repo:**  
You can name the second repo `app_code` for simplicity
When done, run the following command in your terminal

```
git config --global user.name <github user name>
git config --global user.email <github email>
```

### Step 2: CREATE AWS Resources
#### Create an IAM user and generate the AWS Access key
Create a new IAM User on AWS and give it the AdministratorAccess for testing purposes (not recommended for your Organization's Projects)
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
Now, Select your created user then click on `Security credentials` and generate access key by clicking on Create access key.
[image]

Select the `Command Line Interface (CLI)` then select the checkmark for the confirmation and click on Next.
[image]

Provide the Description and click on the Create access key.
[image]

Here, you will see that you got the credentials and also you can download the CSV file for the future. Copy the Access Key ID and the Access Secret Key
[image]

#### Create Github Repo Secret for iac_code
1. **Navigate to Your GitHub Repository:**
   - Find and click on the iac_code repository where you want to add a secret.

2. **Access the Repository Settings:**
   - Click on the "Settings" tab near the top of the repository page.

3. **Open the Secrets Section:**
   - On the left sidebar, click on "Secrets and variables."
   - Then select "Actions" to add a secret available to GitHub Actions.

4. **Add a New Secret:**
   - Click on the "New repository secret" button.
   - Enter the name of your secret in the "Name" field. Use `AWS_ACCESS_KEY_ID`.
   - Enter the value of your secret in the "Value" field. 

5. **Save the Secret:**
   - Click the "Add secret" button to save your new secret.
   - The secret is now stored securely and can be accessed in GitHub Actions workflows using the `${{ secrets.AWS_ACCESS_KEY_ID }}` syntax, where `AWS_ACCESS_KEY_ID` is the name you gave your secret. Do same for the `AWS_SECRET_ACCESS_KEY`, add the Secret and save

6. **Repeat 1-5 for app_code repo:**

#### Create S3 Bucket for Terraform State files 
Create S3 bucket for the terraform state file. Add the bucket name in the iac_code repo secret. Name: `BUCKET_TF_STATE`, Value: `<your-bucket-name>`

#### Copy AWS Account ID
Copy the account ID of your AWS Account. Add your AWS Account ID in the iac_code repo secret. Name: `AWS_ACCOUNT_ID`

#### Create key pair 
Create key pair for SSHing into the jumphost in .pem format and download it in your local machine


### Step 3: Install Terraform & AWS CLI .
Install & Configure Terraform and AWS CLI on your local machine 

#### Terraform Installation Script for WSL
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

#### Terraform and AWSCLI Installation on MacOS
```
brew install terraform
brew install awscli
```

#### Configure AWS CLI

Run the below command, and add your keys from Step 2

`aws configure`
[image]

### Step 4: Deploy the Jumphost Server(EC2) and EKS using Terraform on Github Actions
```
cd ~/Desktop/project/iac_code
```
Open the folder in Visual Studio Code or any Text Editor 
Navigate to the terraform folder

Do some modifications to the `terraform.tf` file such as changing the bucket name (make sure you have created the manually on AWS Cloud). 

[image]

Now, in the `variables.tf` you can change the `region`, `clusterName`, `ami_id`, `instance_type`, but you must replace the `instance_keypair` with the Pem File name as you have for your Pem file. Provide the Pem file name that is already created on AWS.
[image]

Review `.github/workflows/terraform.yml`

```
git commit -m "updated terraform files"
git push
```
With the couple of changed made in the terraform/ folder. 
Github Actions workflow will be trigger. This will take 10-20minutes to deploy the infrastructure

Go to the EC2 on AWS Console
Now, connect to your Jumphost-Server by clicking on Connect.
[image]

Copy the ssh command and paste it on your local machine.
[image]


### Step 5: Configure the Jumphost
We have installed some services such as Docker, Terraform, Kubectl, eksctl, AWSCLI, Trivy, Helm, ArgoCD, Prometheus, Grafana

Let’s validate whether all our tools are installed or not.
```
docker --version
docker ps
terraform --version
kubectl version
aws --version
trivy --version
eksctl --version
```

[image]

#### Create Service Account 
```
eksctl create iamserviceaccount --cluster=quizapp-eks --namespace=kube-system --name=aws-load-balancer-controller --role-name AmazonEKSLoadBalancerControllerRole --attach-policy-arn=arn:aws:iam::<your_aws_account_id>:policy/AWSLoadBalancerControllerIAMPolicy --approve --region=us-east-1
```

Run the below command to deploy the AWS Load Balancer Controller

```
sudo snap install helm --classic
helm repo add eks https://aws.github.io/eks-charts
helm repo update eks
helm install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=quizapp-eks --set serviceAccount.create=false --set serviceAccount.name=aws-load-balancer-controller
```

Wait for 2 minutes and run the following command below to check whether aws-load-balancer-controller pods are running or not.
```
kubectl get deployment -n kube-system aws-load-balancer-controller
```
[image]




### Step 6: Create Docker Repositories for both Frontend & Backend
Sign in into your Dockerhub Account
Click on Create repository
[image]

Select the Public option and provide the name `<backend>` for the repository and click on Create.

Click on Create repository again
Select the Public option and provide the name `<frontend>` for the repository and click on Create.
[image]
 
#### Create Docker Secret
Go to Dockerhub page, click on your profile and select My Account.
Then go to Security and click on New Access Token. Give it a name in the Access Token Description and Generate. Copy the token and add to `app_code` repo secrets, name it `DOCKER_PASSWORD` and paste the docker generated token. Also add another secret name it `DOCKER_USERNAME` and paste your dockerhub account username



### Step 7: Configure Sonar Cloud for our app_code Pipeline
Sonar cloud will be using for Code Quality Analysis of our application code.
Go to `sonarcloud.io` login with your github account. 
Click on + sign on the top right corner

Create New Organization

Create an Organization

Enter a name and key, choose the free plan 

Create Organization

Click om `Analyze a new project`
Enter the values in the image below
[image]

Next.
Previous version

Click on profile

My account

Security

Generate Tokens 

Give it a name 

`Generate Token`

Copy this token to Github app_code repository secret
Name: SONAR_TOKEN
secret: paste the sonarcloud token

Add another secret
Name: SONAR_ORGANIZATION
secret: enter your sonar cloud organization name created above 

Add another secret
Name: SONAR_PROJECT_KEY
secret: enter your sonar cloud project key

Add another secret
Name: SONAR_URL
secret: https://sonarcloud.io


### Step 8: Review and Deploy Application Code
Review the app_code repo.
In your local terminal 
cd ~/Desktop/project/Kubernetes-DevSecOps-CI-CD-Project
Open the folder in Visual Studio Code

Update the kubernetes-manifest/ingress.yaml file with your DNS
Review .github/workflows/quizapp.yml file

```
git commit -m "updated manifest files"
git push
```

### Step 9: Configure ArgoCD
Confirm the namespaces created on the EKS Cluster

```
kubectl get namespaces
```
or 
```
kubectl get ns
```
[image]

To confirm argoCD pods are running.
All pods must be running, to validate run the below command
```
kubectl get pods -n argocd
```
[image]

Now, expose the argoCD server as LoadBalancer using the below command
```
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
```
[image]

You can validate whether the Load Balancer is created or not by going to the AWS Console
[image]

To access the argoCD, copy the LoadBalancer DNS and hit on your browser.

You will get a warning like the below snippet.

Click on Advanced.
[image]

Click on the below link which is appearing under Hide advanced
[image]

Now, we need to get the password for our argoCD server to perform the deployment.

To do that, we need a pre-requisite which is jq. This has already been Installed or you can install it using the command below.
```
sudo apt install jq -y
```
[image]

```
export ARGOCD_SERVER='kubectl get svc argocd-server -n argocd -o json | jq - raw-output '.status.loadBalancer.ingress[0].hostname''
export ARGO_PWD='kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d'
echo $ARGO_PWD
```
[image]

Enter the username and password in argoCD and click on SIGN IN.
[image]

Here is our ArgoCD Dashboard.
[image]



### Step 10: Set up the Monitoring for our EKS Cluster using Prometheus and Grafana. 
We can monitor the Cluster Specifications and other necessary things.
Prometheus and Grafana has already been installed in our jumphost server.

Now, confirm the service by the below command
```
kubectl get svc
```
[image]


Now, we need to access our Prometheus and Grafana consoles from outside of the cluster.

For that, we need to change the Service type from ClusterType to LoadBalancer

Edit the stable-kube-prometheus-sta-prometheus service
```
kubectl edit svc stable-kube-prometheus-sta-prometheus
```
[image]


Modification in the 48th line from ClusterType to LoadBalancer
[image]

Edit the stable-grafana service

```
kubectl edit svc stable-grafana
```
[image]

Modification in the 39th line from ClusterType to LoadBalancer
[image]

Now, if you list again the service then, you will see the LoadBalancers DNS names
```
kubectl get svc
```
[image]

You can also validate from AWS LB console.
[image]

Now, access your Prometheus Dashboard
Paste the <Prometheus-LB-DNS>:9090 in your browser and you will see somwthing like this
[image]

Click on Status and select Target.
You will see a lot of Targets
[image]


Now, access your Grafana Dashboard
Copy the ALB DNS of Grafana and paste it into your browser.
The username will be admin and the password will be prom-operator for your Grafana LogIn.
[image]

Now, click on Data Source
[image]


Select Prometheus
[image]

In the Connection, paste your <Prometheus-LB-DNS>:9090.
[image]

If the URL is correct, then you will see a green notification/
Click on Save & test.
[image]

Now, we will create a dashboard to visualize our Kubernetes Cluster Logs.
Click on Dashboard.
[image]

Once you click on Dashboard. You will see a lot of Kubernetes components monitoring.
[image]

Let’s try to import a type of Kubernetes Dashboard.
Click on New and select Import
[image]

Provide 6417 ID and click on Load
Note: 6417 is a unique ID from Grafana which is used to Monitor and visualize Kubernetes Data
[image]

Select the data source that you have created earlier and click on Import.
[image]

Here, you go.
You can view your Kubernetes Cluster Data.
Feel free to explore the other details of the Kubernetes Cluster.
[image]



### Step 11: Deploy Quiz Application using ArgoCD.

Configure the app_code github repository in ArgoCD.
Click on Settings and select Repositories
[image]

Click on CONNECT REPO USING HTTPS
[image]

Now, provide the repository name where your Manifests files are present.
Provide the username and GitHub Personal Access token and click on CONNECT.
[image]

If your Connection Status is Successful it means repository connected successfully.
[image]

Now, we will create our first application which will be a database.
Click on CREATE APPLICATION.
[image]

Provide the details as it is provided in the below snippet and scroll down.
[image]

Select the same repository that you configured in the earlier step.
In the Path, provide the location where your Manifest files are presented and provide other things as shown in the below screenshot.
Click on CREATE.
[image]

While your database Application is starting to deploy, create an application for the backend.
Provide the details as it is provided in the below snippet and scroll down.
[image]

Select the same repository that you configured in the earlier step.
In the Path, provide the location where your Manifest files are presented and provide other things as shown in the below screenshot.
Click on CREATE.
[image]

While your backend Application is starting to deploy, create an application for the frontend.
Provide the details as it is provided in the below snippet and scroll down.
[image]

Select the same repository that you configured in the earlier step.
In the Path, provide the location where your Manifest files are presented and provide other things as shown in the below screenshot.
Click on CREATE.
[image]

While your frontend Application is starting to deploy, create an application for the ingress.
Provide the details as it is provided in the below snippet and scroll down.
[image]

Select the same repository that you configured in the earlier step.
In the Path, provide the location where your Manifest files are presented and provide other things as shown in the below screenshot.
Click on CREATE.
[image]

Once your Ingress application is deployed. It will create an Application Load Balancer
You can check out the load balancer named with k8s-three.
[image]

Now, Copy the ALB-DNS and go to your Domain Provider in my case AWS Route 53 is the domain provider.

Go to DNS and add a CNAME type with hostname backend then add your ALB in the Answer and click on Save
Note: I have created a subdomain backend.devopsogo.com
[image]

You can see all 4 application deployments in the below snippet.
[image]

Now, hit your subdomain after 2 to 3 minutes in your browser to see the magic.
[image]

You can play with the application by playing the quiz.
[image]


Now, you can see your Grafana Dashboard to view the EKS data such as pods, namespace, deployments, etc.
[image]

If you want to monitor the quiz-app namespace.
In the namespace, replace quiz-app with another namespace.
You will see the deployments that are done by ArgoCD
[image]

This is the Ingress Application Deployment in ArgoCD
[image]

This is the Frontend Application Deployment in ArgoCD
[image]

This is the Backend Application Deployment in ArgoCD
[image]

This is the Database Application Deployment in ArgoCD
[image]

If you observe, we have configured the Persistent Volume & Persistent Volume Claim. So, if the pods get deleted then, the data won’t be lost. The Data will be stored on the host machine.
To validate it, delete both Database pods.
[image]

Now, the new pods will be started.
[image]

And Your Application won’t lose a single piece of data.
[image]


### Conclusion: 
In this comprehensive DevSecOps Kubernetes project, we successfully:

- Established IAM user and Terraform for AWS setup.
- Deployed Infrastructure on AWS using Github Actions and Terraform and, configured tools.
- Set up an EKS cluster, and configured a Load Balancer.
- Implemented monitoring with Helm, Prometheus, and Grafana.
- Installed and configured ArgoCD for GitOps practices.
- Created Github Action pipelines for CI/CD, deploying a three-tier architecture application.
- Ensured data persistence with persistent volumes and claims.

Stay connected on LinkedIn: LinkedIn Profile
Stay up-to-date with GitHub: GitHub Profile
Feel free to reach out to me, if you have any other queries.
Happy Coding!
