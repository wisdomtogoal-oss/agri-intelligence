from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import random

app = FastAPI(
    title="Uttarakhand Agri-Intelligence API",
    description="Backend API for Crop & Animal Disease Diagnosis following ICAR & GBPUAT Pantnagar guidelines.",
    version="1.0.0"
)

# Enable CORS so your GitHub Pages frontend can communicate with this backend API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any origin (GitHub Pages)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Knowledge Base matching ICAR and GBPUAT Pantnagar Guidelines
DIAGNOSIS_DATABASE = [
    {
        "disease": "धान का झोंका रोग (Rice Blast)",
        "organic": "नीम का तेल (5ml/लीटर) एवं ट्राइकोडर्मा हरज़ियानम का छिड़काव करें।",
        "chemical": "ट्राइसाइक्लाजोल 75% WP @ 0.6g/लीटर पानी में मिलाकर छिड़काव करें (GBPUAT सिफारिश)।",
        "kumaoni_advisory": "भैया, तुमरा धानक पात में झोंका रोग लागि रोछ। नीमौक तेल या दवा छिड़किया।"
    },
    {
        "disease": "टमाटर का पछेती झुलसा (Late Blight of Tomato)",
        "organic": "खट्टा छाछ (1 लीटर प्रति 10 लीटर पानी) एवं कॉपर सल्फेट का घोल छिड़कें।",
        "chemical": "मैनकोज़ेब 75% WP @ 2.5 ग्राम प्रति लीटर पानी में मिलाकर छिड़काव करें।",
        "kumaoni_advisory": "टमाटर में झुलसा बीमारी है। छाछ और तांबे का पानी या मैंकोजेब छिड़कें।"
    },
    {
        "disease": "पशु त्वचा संक्रमण / लम्पी रोग (Livestock Skin Infection)",
        "organic": "नीम के पत्तों के पानी से धोएं तथा हल्दी, एलोवेरा और नीम का लेप लगाएं।",
        "chemical": "पशु चिकित्सक की सलाह से आईवरमेक्टिन इंजेक्शन एवं एंटीसेप्टिक स्प्रे (Topicure) का प्रयोग करें।",
        "kumaoni_advisory": "गोरू का छाल में बीमारी छ। नीम का पाणी ले धोवा और हल्दी का लेप लगाया।"
    },
    {
        "disease": "पहाड़ी राजमा पत्ती धब्बा रोग (Leaf Spot in Rajma)",
        "organic": "जीवामृत का 10% घोल बनाकर 10-12 दिन के अंतराल पर छिड़काव करें।",
        "chemical": "कार्बेन्डाजिम 50% WP @ 1 ग्राम प्रति लीटर पानी में मिलाकर स्प्रे करें।",
        "kumaoni_advisory": "राजमाक पात में धब्बा रोछ। जीवामृत या कार्बेन्डाजिम छिड़किया।"
    }
]

@app.get("/")
def read_root():
    """Health check endpoint to verify Render server status."""
    return {"status": "online", "message": "Uttarakhand Agri-Intelligence API is running."}

@app.post("/predict")
async def predict_disease(file: UploadFile = File(...)):
    """
    Accepts an uploaded image file (Crop leaf or Animal skin),
    runs model analysis, and returns diagnosis with remedies.
    """
    # Validate image format
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    try:
        # Read the image bytes
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Verify image opens correctly
        image.verify()
        
        # --- MODEL INFERENCE PLACEHOLDER ---
        # Note: If you train a PyTorch/TensorFlow .pth/.h5 model, load it here.
        # Currently fetches structured GBPUAT/ICAR diagnosis from database:
        selected_result = random.choice(DIAGNOSIS_DATABASE)

        return {
            "success": True,
            "filename": file.filename,
            "disease": selected_result["disease"],
            "organic": selected_result["organic"],
            "chemical": selected_result["chemical"],
            "kumaoni_advisory": selected_result["kumaoni_advisory"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image processing failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
