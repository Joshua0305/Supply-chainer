from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import joblib
import pandas as pd
from nlp_engine import SupplyChainNLP

app = FastAPI(title="Dynamic Risk API", description="Context-Aware Supply Chain Routing Engine")

print("Booting up AI Models...")
risk_model = joblib.load('risk_model.pkl')
encoders = joblib.load('label_encoders.pkl')
nlp_processor = SupplyChainNLP()

class RouteRequest(BaseModel):
    Leg_Type: str
    Origin_Node: str
    Destination_Node: str
    Transport_Mode: str
    Condition_Flag: str
    Live_News_Feed: dict 

@app.post("/predict_route_risk")
def predict_risk(request: RouteRequest):
    try:
        max_final_threat = 0.0
        threat_logs = {}

        for loc, live_news in request.Live_News_Feed.items():
            
            raw_score = nlp_processor.generate_severity_score(live_news)
            
            relevance = nlp_processor.calculate_relevance(
                news_text=live_news,
                mode=request.Transport_Mode,
                origin=request.Origin_Node,
                destination=request.Destination_Node
            )
            
            node_threat = raw_score * relevance
            threat_logs[loc] = {"news_analyzed": live_news, "calculated_threat": round(node_threat, 3)}
            
            if node_threat > max_final_threat:
                max_final_threat = node_threat

        data = {
            'Leg_Type': [request.Leg_Type],
            'Origin_Node': [request.Origin_Node],
            'Destination_Node': [request.Destination_Node],
            'Transport_Mode': [request.Transport_Mode],
            'Condition_Flag': [request.Condition_Flag],
            'NLP_Severity_Score': [max_final_threat] # The max threat from the live news!
        }
        df_input = pd.DataFrame(data)

        for col in ['Leg_Type', 'Origin_Node', 'Destination_Node', 'Transport_Mode', 'Condition_Flag']:
            if df_input[col][0] in encoders[col].classes_:
                df_input[col] = encoders[col].transform(df_input[col])
            else:
                df_input[col] = encoders[col].transform([encoders[col].classes_[0]])

        prediction = risk_model.predict(df_input)[0]
        final_delay_hours = max(0.0, float(prediction))

        return {
            "status": "success",
            "route_max_threat_score": round(max_final_threat, 3),
            "predicted_worst_case_delay_hours": round(final_delay_hours, 2),
            "threat_logs": threat_logs,
            "message": "Dynamic risk weight calculated successfully."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))