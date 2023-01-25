# let-me-help
Intelligent Interactive Systems course final project

An interactive app which helps you to stop overthinking about thing and make a decision.

Have you ever had the feeling where you want to see a movie, or buy a gift, or go on a vacation, or something else, but you're not sure on which direction to go? Do you somtime feel like the web is so full of interesting ideas that you're having hard time choosing things?
### Let Me Help you!
Use this app to get recommendations or help you decide between options, based on your current mood. 

## How To Run
1. Download the repository
1. Download the file in [this link](https://drive.google.com/file/d/1ssIMDYn_c6oU7bfneE-YYSszLNVxBTOC/view?usp=sharing) and unzip it in the root folder of the repository (from step 1).
1. Open terminal and navigate to the downloaded directory
1. Create a virtual environment using the following command: `python -m venv .venv` and activate it with `source .venv/bin/activate` 
(or with `.venv\Scripts\activate.bat` on Windows)
1. Install requirements by running `pip install -r requirements.txt`
1. Run `streamlit run let_me_help.py` to start the app. The app will open in your browser.

## How to use
First, you'll have to choose what kind of help you need:
1. If you would like to get ideas for a specific domain you have in mind (e.g vacation destination, gift, movie, etc.), click on "I want recommendations" button. 
2. If you're having trouble to decide between 2 options (of any kind) click on "Help me decide" button.
![Initial view](https://user-images.githubusercontent.com/48162535/214577905-2156fb85-d63e-4cd8-bd63-03872208c19c.png)*Initial view*


### 1. Get Recommendations
If you choose to get recommendations, you'll next have to choose the domain in which you need recommendations for from the dropdown, then click "Start".
![recommendation](https://user-images.githubusercontent.com/48162535/214580772-26272e54-9c53-49c3-8e22-83c8f15a7c39.png)*Get recommendations*

### 2. Get Help Making a Decision
If you choose to get help deciding, you'll next have to enter 2 options from which you need to pick 1. These could be anything you want. Then click "Start".
![decide](https://user-images.githubusercontent.com/48162535/214582153-9c4842a4-df91-4485-a3a0-72ef28d4e87f.png)*Get help with a decision*

### The Questions Phase
Once "Start" button is clicked, you will face a series of questions, on each one two images will be shown, and you'll to select which one you like better by clicking the "Choose This" button below it. A progress bar shows the progress in this phase.
![questions](https://user-images.githubusercontent.com/48162535/214643604-41a1a47a-4a3a-4173-ba63-083253c6f427.png)*Question phase*

