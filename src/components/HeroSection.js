import React from "react";
import "../App.css";
import "./HeroSection.css";
import CustomPieChart from "./PieChart";

function HeroSection({setMood}) {
  return (
    <div className="hero-container">
      <video src="/videos/video-3.mp4" autoPlay loop muted />
      <div className="image-container">
        <CustomPieChart setMood = {setMood}/>
      </div>
    </div>
  );
}

export default HeroSection;
