## Challenge 4: Create an Image Analysis Web App using Azure AI Vision

## Overview

⏲️ **Exercise duration:**
*Estimated time to complete the exercise: 60 minutes*

🎯 **Exercise objectives**:

* Build a Streamlit Web App that consumes **Azure AI Vision** for image analysis.
* Understand how to consume a cloud AI service: create the resource, get the secrets, call the API.
* **(Bonus)** Deploy the Web App to Azure with a CI/CD approach.

🔧 **Tools**:

* **VS Code** for interactive coding
* **Streamlit** to build Web Apps
* **Azure AI Vision** for image analysis
* **GitHub** to host the code of your Apps

---
## 📃 Instructions

In this challenge, you will build a Streamlit Web App that performs image analysis with the Azure AI Vision API. By the end of this exercise, you will understand how to consume an Azure AI service from python.

### 1. Build a simple version of your Web App locally

- Open `Anaconda Prompt` using the `streamlit-env` environment you created during the setup:

<figure style="width: 90%">
  <img alt="Open a terminal with the streamlit-env environment" src="https://learn.lewagon.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNjk0Qmc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--17c1ad93ffc67fd6aaacdc90682e5c205ece9ecf/Anaconda-Navigator-environment-6-activate.png" />
</figure>

- Create a new project directory next to your other projects (use a unique name, e.g. your first name):

  ```bash
  cd Documents/GitHub
  mkdir yourimageanalysisapp
  cd yourimageanalysisapp
  ```

<figure style="width: 80%">
  <img alt="Change to the GitHub projects directory" src="https://learn.lewagon.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBK2w0Qmc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--76adb1aa94aabc3857ba7e64c956edeb4bd248c0/streamlit-env-4.png" />
</figure>

- Create a new Python file `app.py`:

  ```bash
  # macOS / Linux
  touch app.py
  ```

  ```cmd
  # Windows (Anaconda Prompt / cmd)
  type nul > app.py
  ```

- Open it in VS Code with the `streamlit-env` and paste:

  ```python
  import streamlit as st

  # this is the main function in which we define our webpage
  def main():
      st.markdown("# Image Analysis App 🖼️")
      st.markdown("### This app allows you to extract visual features from images.")

  # Init code
  if __name__=='__main__':
      main()
  ```

- Run it:

  ```bash
  streamlit run app.py
  ```

The app opens in your browser (typically http://localhost:8501). You should see the two titles. Close it (`Ctrl + C`) and go back to VS Code.

---
### 2. Create your Azure AI Vision resource

`Azure AI Vision` gives you access to AI algorithms for image processing: OCR (text extraction), image analysis (objects, tags, descriptions), face detection, and more.

You will create the resource yourself, get its **key** and **endpoint**, and use them from python.

- Go to the [Azure Portal](https://portal.azure.com) → **Create a resource** → search **Computer Vision** → Create.

<figure style="width: 50%">
  <img alt="Computer Vision resource list - click Create" src="https://learn.lewagon.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNEFOQnc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--947a8cf1367b666bacf86dad605aefd425e9e3ad/Capture%20d%E2%80%99e%CC%81cran%202026-06-14%20a%CC%80%2020.36.31.png" />
</figure>

- In the **Basics** tab:
  - **Subscription**: `AI_Integration`
  - **Resource group**: your resource group (your first name)
  - **Region**: **France Central**
  - **Name**: use your first name, e.g. `yourname-vision`
  - **Pricing tier**: **Standard S0**

  🧠 **Why Standard S0 and not Free F0?** Azure only allows **one Free (F0) Computer Vision resource per region per subscription** — with a whole group sharing one subscription, the second person to pick F0 would get an error. S0 is pay-per-call (a few cents per thousand transactions) and has no such limit, so everyone can have their own. For this exercise the cost is negligible. **Don't forget**: your teacher will clean up these resources after the training.

<figure style="width: 50%">
  <img alt="Create Computer Vision - Basics tab with resource group and pricing tier" src="https://learn.lewagon.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNEVOQnc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--dc1f130a327263dd78af6e76a38b4f1fabe7c1a0/Capture%20d%E2%80%99e%CC%81cran%202026-06-14%20a%CC%80%2020.36.58.png" />
</figure>

- Keep defaults for the other tabs, then **Review + Create**.

- Open your new resource → **Keys and Endpoint**. Copy **KEY 1** and the **Endpoint** — you need them for the app.

<figure style="width: 50%">
  <img alt="Vision resource overview - Keys and endpoint" src="https://learn.lewagon.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNElOQnc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--caca8d5352d6d1b0b57ba7e7345392bab5e0cec8/Capture%20d%E2%80%99e%CC%81cran%202026-06-14%20a%CC%80%2020.37.48.png" />
</figure>


---
### 3. Build the Image Analysis Web App

- In your project folder, install the required libraries in the `streamlit-env`:

  ```bash
  pip install python-dotenv pillow azure-ai-vision-imageanalysis
  ```

  > 💡 We use the current `azure-ai-vision-imageanalysis` SDK (the older `azure-cognitiveservices-vision-computervision` package is legacy).

- ⚠️ **Create a `.gitignore` FIRST**, before the `.env`:

  ```text
  .env
  __pycache__
  .DS_Store
  ```

  🧠 **Why first?** Your `.env` will contain a live API key. If you commit and push it to GitHub, the key is public and anyone can use it on your Azure resource. Leaked keys are one of the most common real-world cloud security incidents. The `.gitignore` guarantees git never picks it up. **Never commit secrets.**

- Create a `.env` file with your secrets:

  ```text
  VISION_KEY="your_key"
  VISION_ENDPOINT="your_endpoint"
  ```

- Load the secrets in `app.py` (organize imports at the top):

  ```python
  import os
  from dotenv import load_dotenv

  # loading variables from .env file
  load_dotenv()

  # accessing vision key and endpoint
  vision_key = os.getenv("VISION_KEY")
  vision_endpoint = os.getenv("VISION_ENDPOINT")

  # Quick check that the secrets are loaded — REMOVE these two lines once it works,
  # never display an API key in a real app!
  # st.text(vision_key)
  # st.text(vision_endpoint)
  ```

  > ⚠️ Notice the check lines are **commented out**. If you want to verify your secrets load, uncomment them *temporarily*, then comment them again. Displaying a key on screen (or worse, in a deployed app) is exactly the kind of leak we want to avoid.

- Authenticate the client and analyse an image. Add this to `app.py`:

  ```python
  from azure.ai.vision.imageanalysis import ImageAnalysisClient
  from azure.ai.vision.imageanalysis.models import VisualFeatures
  from azure.core.credentials import AzureKeyCredential

  # Create the Image Analysis client
  client = ImageAnalysisClient(
      endpoint=vision_endpoint,
      credential=AzureKeyCredential(vision_key)
  )

  def main():
      st.markdown("# Image Analysis App 🖼️")
      st.markdown("### This app allows you to extract visual features from images.")

      # A real, direct image URL (note: a Wikipedia *article* URL is NOT an image —
      # you need the direct link to the .jpg file)
      image_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/faces.jpg"


      st.image(image_url, caption="Image to analyse")

      if st.button("Analyse image"):
          result = client.analyze_from_url(
              image_url=image_url,
              visual_features=[VisualFeatures.TAGS, VisualFeatures.CAPTION]
          )

          # Caption: a one-sentence description of the image
          if result.caption is not None:
              st.markdown(f"**Caption:** {result.caption.text} "
                          f"(confidence {result.caption.confidence:.2%})")

          # Tags: detected concepts with confidence
          st.markdown("**Tags detected:**")
          if result.tags is not None:
              for tag in result.tags.list:
                  st.text(f"'{tag.name}' — confidence {tag.confidence:.2%}")

  if __name__=='__main__':
      main()
  ```

- Run the app, click **Analyse image**. You should see a caption and a list of tags with confidence scores. 🎉

<figure style="width: 100%">
  <img alt="Streamlit app showing the image analysis result with tags" src="https://learn.lewagon.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBN3FIQmc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--d1299664ef260ee7c534b7311e41493a147dcccd/Capture%20d'%C3%A9cran%202024-09-23%20144702.png" />
</figure>

  🧠 Notice you sent only a URL and got back a structured analysis — your app holds no model, it *consumes* a cloud AI service. Same Front-End / Back-End separation as the wine app, except the "back-end" is a managed Azure service this time.

---
### 4. Bonus Challenges

- **Analyse any image from the web**: add a `st.text_input` so the user pastes an image URL, display it with `st.image`, and analyse it on a button click.

- **Analyse a local image**: use `st.file_uploader` to let the user upload an image, then call `client.analyze(image_data=...)` instead of `analyze_from_url`. See the [documentation](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/how-to/call-analyze-image-40?tabs=python).

- **Try other visual features**: add `VisualFeatures.OBJECTS` (bounding boxes), `VisualFeatures.READ` (OCR — extract text from an image), `VisualFeatures.PEOPLE`. Which feature fits which use case?

- **Explore the Vision Studio gallery**: before coding, you can try Vision features interactively (no code) in the official demo gallery, including the [Face gallery](https://portal.vision.cognitive.azure.com/gallery/face) (detection, attributes, liveness). 🧠 Note that some **Face** capabilities (like face identification/recognition) are **Limited Access** features: Microsoft requires an eligibility request before you can use them in your own resource. The gallery lets you *see* what they do without that approval — good for understanding the service's scope.

- **Deploy to Azure**: deploy this Streamlit app to Azure App Service on your existing plan, with CI/CD — exactly as you did for the wine UI in Challenge 2. (Remember: the `.env` is gitignored, so on Azure you set `VISION_KEY` and `VISION_ENDPOINT` as **App Settings** in the Web App configuration, not in a file.)

  🧠 This last point is important: in production, secrets never travel in your repo. They live in the platform's configuration (App Settings, Key Vault...). The `.env` is a *local-development* convenience only.

---

Congratulations! You have built a Web App that consumes Azure AI Vision. 🎉

### Don't forget to save your work!

Save your files: File > Save. Then close all the tabs in your browser and VS Code windows. You can safely close the Anaconda Prompt.

💡 Don't forget to **push your code to GitHub** — and check that **`.env` is NOT in the pushed files**.

1. Open GitHub Desktop.
2. It should automatically detect any file with modifications.
3. Make sure these files are ticked (and `.env` is not there!), and write a _commit message_.
4. Click **Commit to `master`**, then **Push `origin`**.

---
## 🥇 Key learning points

By the end of this exercise, you will have:

* Created an Azure AI Vision resource and retrieved its developer secrets.
* Consumed the Vision API from a Streamlit app using the current SDK.
* Handled API **secrets properly** with a gitignored `.env` locally, and understood that production secrets live in platform configuration.

That's it! Take a small break before diving into the next exercise.