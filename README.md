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
2. Infrastructure as Code (IaC): Use Terraform and AWS CLI to set up the Jumphost server (EC2 instance) on AWS.
3. Github Actions Configuration: configure essential githubt actions on Github Actions workflow, including Snyk, Docker, Sonarqube, Terraform, Kubectl, AWS CLI, and Trivy.
4. EKS Cluster Deployment: Utilize eksctl commands to create an Amazon EKS cluster, a managed Kubernetes service on AWS.
5. Load Balancer Configuration: Configure AWS Application Load Balancer (ALB) for the EKS cluster.
6. Dockerhub Repositories: Automatically Create repositories for both frontend and backend Docker images on Dockerhub.
7. ArgoCD Installation: Install and set up ArgoCD for continuous delivery and GitOps.
8. Sonarqube Integration: Integrate Sonarqube for code quality analysis in the DevSecOps pipeline.
9. Snyk Integration: Integrate Snyk for vulnerability scanning and dependency management analysis in the DevSecOps pipeline.
10. Trivy Integration: Integrate Trivy for container image and filesystem vulnerability scanning in the DevSecOps pipeline.
11. Github Action Pipelines: Create Github Action pipelines for deploying backend and frontend code to the EKS cluster.
12. Monitoring Setup: Implement monitoring for the EKS cluster using Helm, Prometheus, and Grafana.
13. ArgoCD Application Deployment: Use ArgoCD to deploy the Three-Tier application, including database, backend, frontend, and ingress components.
14. DNS Configuration: Configure DNS settings to make the application accessible via custom subdomains.
15. Data Persistence: Implement persistent volume and persistent volume claims for database pods to ensure data persistence.
16. Conclusion and Monitoring: Conclude the project by summarizing key achievements and monitoring the EKS cluster’s performance using Grafana.

### Prerequisites:
Before starting this project, ensure you have the following prerequisites:

- An AWS account with the necessary permissions to create resources.
- Terraform and AWS CLI installed on your local computer.
- Basic familiarity with Kubernetes, Docker, CICD pipelines, Github Actions, Terraform, and DevOps principles.

### Step 1: SSH Exchange between local computer and Github account
`cd` to home dir and create .ssh/ folder if it doesn't exist 

```
cd ~/.ssh
ssh-keygen
```
Give the key a name `key`. Then list `ls` the content of .ssh/ folder.

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
git clone https://github.com/cloudcore-hub/reactjs-quiz-app.git
```
```
git clone https://github.com/cloudcore-hub/iac_code.git
```
```
cd iac_code
git config core.sshCommand "ssh -i ~/.ssh/key -F /dev/null"
```
```
cd ..
cd reactjs-quiz-app
git config core.sshCommand "ssh -i ~/.ssh/key -F /dev/null"
```
#### Connect the repository to your Github

1. **Create a New Repository on GitHub:**
   - Go to GitHub and sign in.
   - Go to your profile and open Your repositories
   - Click the `New` icon in the top-right corner to create new repository.
   - Name your repository `iac`, set it to public or private, and click "Create repository."

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
You can name the second repo `reactjs` for simplicity
When done, run the following command in your terminal

```
git config --global user.name <your github user name>
git config --global user.email <your github email>
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

Click on Next.

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

#### Create Github Repo Secret for iac
1. **Navigate to Your GitHub Repository created in step 1:**
   - Find and click on the iac repository where you want to add a secret.

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

6. **Repeat 1-5 for app code repository:**

#### Create S3 Bucket for Terraform State files 
Create S3 bucket for the terraform state file. Add the bucket name in the iac_code repo secret. Name: `BUCKET_TF`, Value: `<your-bucket-name>`


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

### Step 4: Deploy the Jumphost Server(EC2) using Terraform on Github Actions
```
cd ~/Desktop/project/iac_code
```
Open the folder in Visual Studio Code or any Text Editor 
Navigate to the terraform folder

Do some modifications to the `terraform.tf` file such as changing the bucket name (make sure you have created the bucket manually on AWS console). 

[image]

Now, in the `variables.tf` you can change some of the variable `region`, `vpc-name`, `ami_id`, `instance_type`, but you must replace the `instance_keypair` with the Pem File name as you have for your Pem file. Provide the Pem file name that is already created on AWS.
[image]

Review `.github/workflows/terraform.yml`

```
git commit -am "updated terraform files"
git push
```
With the couple of changed made in the terraform/ folder. 
Github Actions workflow will be trigger. 
Go to the repo on Github abd click on the Actions button to the see the Github Action workflow running.

Go to the EC2 on AWS Console
Now, connect to your Jumphost-Server by clicking on Connect.
[image]

Copy the ssh command and paste it on your local machine.
Be sure you are in the same folder where your key pair is saved or provide the path to the key. For first time use incase of file permission error, run 
```
Chmod 400 key.pem
```
and try SSHing again
[image]


### Step 5: Configure the Jumphost
We have installed some services such as Docker, Terraform, Kubectl, eksctl, AWSCLI, Trivy

Validate whether all our tools are installed or not.
```
docker --version
docker ps
terraform --version
kubectl version
aws --version
trivy --version
eksctl version
```

[image]

#### Create an eks cluster using the below commands.
This might take 15-20 minutes. Also adjust the node count 
```
eksctl create cluster --name quizapp-eks-cluster --region us-east-1 --node-type t2.large --nodes-min 2 --nodes-max 4
```

Run the command below to connect to the EKS cluster created  allowing Kubernetes operations on that cluster.
```
aws eks update-kubeconfig --region us-east-1 --name quizapp-eks-cluster
```

Once the cluster is created, you can validate whether your nodes are ready or not by the below command

```
kubectl get nodes
```

#### Configure Load Balancer on the EKS
Configure the Load Balancer on our EKS because our application will have an ingress controller.
Download the policy for the LoadBalancer prerequisite.

```
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.5.4/docs/install/iam_policy.json
```
#### Create IAM policy
Create the IAM policy using the below command
```
aws iam create-policy --policy-name AWSLoadBalancerControllerIAMPolicy --policy-document file://iam_policy.json
```
#### Create OIDC Provider
To allows the cluster to integrate with AWS IAM for assigning IAM roles to Kubernetes service accounts, enhancing security and management.
```
eksctl utils associate-iam-oidc-provider --region=us-east-1 --cluster=quizapp-eks-cluster --approve
```
#### Create Service Account 
Add your aws 12-digit account ID
```
eksctl create iamserviceaccount --cluster=quizapp-eks-cluster --namespace=kube-system --name=aws-load-balancer-controller --role-name AmazonEKSLoadBalancerControllerRole --attach-policy-arn=arn:aws:iam::<ACCOUNT-ID>:policy/AWSLoadBalancerControllerIAMPolicy --approve --region=us-east-1
```

Run the below command to deploy the AWS Load Balancer Controller using Helm

```
sudo snap install helm --classic
helm repo add eks https://aws.github.io/eks-charts
helm repo update eks
helm install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=quizapp-eks-cluster --set serviceAccount.create=false --set serviceAccount.name=aws-load-balancer-controller
```

Wait for 2 minutes and run the following command below to check whether aws-load-balancer-controller pods are running or not.
```
kubectl get deployment -n kube-system aws-load-balancer-controller
```
[image]



### Step 6: Setup Docker Repositories to allow image push for  Frontend & Backend images
Sign in into your Dockerhub Account
Click on Create repository

#### Create Docker Secret
Go to Dockerhub page, click on your profile and select My Account.
Then go to Security and click on New Access Token. Give it a name in the Access Token Description and Generate. Copy the token and add to `app` repo secrets, name it `DOCKER_PASSWORD` and paste the docker generated token. Also add another secret name it `DOCKER_USERNAME` and paste your dockerhub account username



### Step 7: Configure Sonar Cloud for our app_code Pipeline
Sonar cloud will be using for Code Quality Analysis of our application code.

#### 1. Create a SonarCloud Account

- Go to [SonarCloud](https://sonarcloud.io/) and click on **Sign up**.
- Choose the option to sign up using GitHub, Bitbucket, or GitLab.
- Follow the prompts to authorize SonarCloud to access your account.

#### 2. Create a New Public Organization

- Once logged in, go to **+** (top-right corner) and select **Create new organization**.
- Choose the service where your code is hosted (GitHub, Bitbucket, GitLab).
- Follow the on-screen instructions to select your account and set up a new organization.
- Choose **Public** for the organization’s visibility.

#### 3. Create a Project

- In your new organization, click on **+** and select **Analyze new project**. Enter name and key. Then clikc on previous version and save

#### 4. Create a Token

- Go to **My Account > Security**.
- Under **Tokens**, enter a name for your new token and click **Generate**.
- Save the generated token securely. You will use this token in your analysis commands or CI/CD configuration.

**Note**: Keep your token confidential and use it as per the instructions for analyzing your project, either locally using SonarScanner or through your CI/CD pipeline.


Copy this token to Github app code repository secret
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

### Step 8: Setup Synk Token for the app code pipeline 

#### 1. Sign Up for Snyk
- Visit the [Snyk website](https://snyk.io) and click on the "Sign Up" button.
- You can sign up using your GitHub, GitLab, Bitbucket account, or an email address.

#### 2. Verify Your Email
- If you signed up with an email, verify your email address by clicking on the verification link sent to your email.

#### 3. Log in to Your Snyk Account
- After verifying your email or signing up through a version control system, log in to your Snyk account.

#### 4. Generate a Snyk Token
- Navigate to the account settings or your profile settings.
- Look for the API tokens section.
- Click on "Generate Token" or "Create New Token."
- Name your token and, if given the option, set the scopes or permissions for the token.
- Click "Generate" or "Create."

#### 5. Secure Your Token
- Copy the generated token and keep it secure. Do not share your token in public places.

You can now use this token to authenticate and integrate Snyk with your projects or CI/CD pipelines.

Copy this token to Github app code repository secret
Name: SNYK_TOKEN
secret: paste the snyk token


### Step 8: Review and Deploy Application Code
Review the app code repo.
In your local terminal 
cd ~/Desktop/project/reactjs-quiz-app
Open the folder in Visual Studio Code

Update the kubernetes-manifest/ingress.yaml file with your DNS
Review .github/workflows/quizapp.yml file

```
git commit -am "updated manifest files"
git push
```

### Step 9: Configure ArgoCD
Create the namespace for the EKS Cluster. In your jumphost server terminal 

```
kubectl create namespace quiz
kubectl get namespaces
```
or 
```
kubectl get ns
```
[image]

Now, we will install argoCD.
To do that, create a separate namespace for it and apply the argocd configuration for installation.

```
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v2.4.7/manifests/install.yaml
```

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
export ARGOCD_SERVER=`kubectl get svc argocd-server -n argocd -o json | jq --raw-output '.status.loadBalancer.ingress[0].hostname'`
export ARGO_PWD=`kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d`
echo $ARGO_PWD
```
[image]

Enter the username `admin` and password in argoCD and click on SIGN IN.
[image]

Here is our ArgoCD Dashboard.
[image]



### Step 10: Set up the Monitoring for our EKS Cluster using Prometheus and Grafana. 
We can monitor the Cluster Specifications and other necessary things.

We will achieve the monitoring using Helm
Add all the helm repos, the prometheus, grafana repo by using the below command
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
```

Install the prometheus
```
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
```

Install the Grafana 
```
helm install grafana grafana/grafana -n monitoring --create-namespace
```
Get `admin` user password 
```
kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```




Install ingress-nginx
```
helm install ingress-nginx ingress-nginx/ingress-nginx
```
Now, confirm the service by the below command
```
kubectl get svc -n monitoring
```
[image]


Now, we need to access our Prometheus and Grafana consoles from outside of the cluster.

For that, we need to change the Service type from ClusterIP to LoadBalancer

Edit the prometheus-server service
```
kubectl edit svc prometheus-kube-prometheus-prometheus -n monitoring
```
[image]


Modification in the 48th line from ClusterIP to LoadBalancer
[image]

Edit the Grafana service

```
kubectl edit svc grafana -n monitoring
```
[image]

Modification in the 39th line from ClusterIP to LoadBalancer
[image]

Now, if you list again the service then, you will see the LoadBalancers DNS names
```
kubectl get svc -n monitoring
```
[image]

You can also validate from AWS LB console.
[image]

Now, access your Prometheus Dashboard
Paste the <Prometheus-LB-DNS>:9090 in your browser and you will see something like this
[image]

Click on Status and select Target.
You will see a lot of Targets
[image]


Now, access your Grafana Dashboard
Copy the ALB DNS of Grafana and paste it into your browser.

Get your 'admin' user password by running:
```
kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

The username will be admin and the password will be from the command above for your Grafana LogIn.
[image]

Now, click on Data Source
[image]


Select Prometheus
[image]

In the Connection, paste your <Prometheus-LB-DNS>:9090
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
You can check out the load balancer named with k8s-ingress.
[image]

Now, Copy the ALB-DNS and go to your Domain Provider in this case AWS Route 53 is the domain provider.


### Creating an A-Record in AWS Route 53 Using ALB DNS
Create A-records using DNS service in aws [Route53].
Follow these steps to create an A-record in AWS Route 53 that points to your Application Load Balancer (ALB).

#### 1: Open Route 53 Dashboard

In the search bar at the top, type "Route 53" and click on the Route 53 service to open the Route 53 dashboard.

#### 2: Select Hosted Zone

From the Route 53 dashboard, choose "Hosted zones" under the DNS management section. Then select the hosted zone where you want to add the A-record.

#### 3: Create Record

- Click on the "Create record" button.
- In the "Record name" field, enter the subdomain or leave it blank for the root domain.
- For "Record type", select "A – Routes traffic to an IPv4 address and some AWS resources".
- In the "Value/Route traffic to" section, choose "Alias to Application and Classic Load Balancer".
- Select the region where your ALB is located.
- Choose the ALB (it's identified by its DNS name) from the dropdown.
- (Optional) Adjust the "Routing policy" and "Record ID" as needed.

#### 4: Confirm and Create

Review your configurations and click on the "Create records" button to create your A-record.

By following these steps, you'll successfully create an A-record in AWS Route 53 that points to your Application Load Balancer, allowing you to route traffic from your domain to your ALB.
 

Share the quizapp.cloudcorehub.com

Note: I have created a subdomain quizapp.cloudcorehub.com
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

### Clean up 
From your jumphost server terminal run
```
eksctl delete cluster --name=quizapp-eks-cluster --region=us-east-1
```

In your iac_code terminal, 
cd into the terraform folder
run
```
terraform init -backend-config="bucket=cloudcore007"
```
and then 
```
terraform destroy -auto-approve
```

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
