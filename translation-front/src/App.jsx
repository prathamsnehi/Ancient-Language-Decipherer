import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, Camera, ArrowRight, RefreshCw, AlertCircle, BookOpen, ScrollText, Landmark } from 'lucide-react';

// Use the environment variable if available (Vercel), otherwise fallback to local development
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/translate";

export default function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  
  const fileInputRef = useRef(null);

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    setSelectedImage(file);
    setPreviewUrl(URL.createObjectURL(file));
    setResult(null);
    setError(null);
  };

  const handleTranslate = async () => {
    if (!selectedImage) return;

    setIsLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('image', selectedImage);

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        body: formData,
        // Don't set Content-Type header, let browser set it with the boundary for FormData
      });

      if (!response.ok) {
        throw new Error('Failed to translate image. Please try again.');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'An error occurred while connecting to the translation server.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="min-h-screen pb-20 pt-12 px-4 md:pt-24 md:px-8">
      <main className="max-w-2xl mx-auto space-y-12">
        
        {/* Header Section */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center space-y-4"
        >
          <div className="inline-flex items-center justify-center p-3 bg-primary/10 rounded-full mb-4 text-primary">
            <Camera className="w-6 h-6" />
          </div>
          <h1 className="text-4xl md:text-5xl font-rounded font-bold tracking-tight text-foreground text-balance">
            Voices of the <span className="text-primary">Silent 99%</span>
          </h1>
          <p className="text-lg text-muted-foreground max-w-lg mx-auto text-balance">
            Upload an image of an ancient Egyptian hieroglyph to instantly reveal its literal meaning, modern summary, and historical context.
          </p>
        </motion.div>

        {/* Interactive Area */}
        <div className="relative">
          <AnimatePresence mode="wait">
            {!previewUrl ? (
              /* Upload State */
              <motion.div
                key="upload"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                transition={{ duration: 0.3 }}
                className="bg-surface rounded-4xl p-8 shadow-soft border border-primary/10 flex flex-col items-center justify-center min-h-[300px] text-center cursor-pointer hover:shadow-hover transition-all duration-300"
                onClick={() => fileInputRef.current?.click()}
              >
                <div className="w-20 h-20 bg-muted rounded-full flex items-center justify-center mb-6 text-primary">
                  <Upload className="w-8 h-8" />
                </div>
                <h3 className="text-xl font-rounded font-semibold mb-2">Tap to Capture</h3>
                <p className="text-muted-foreground max-w-xs">
                  Take a photo of a hieroglyph or choose one from your camera roll.
                </p>
                <input 
                  type="file" 
                  ref={fileInputRef}
                  className="hidden" 
                  accept="image/*"
                  onChange={handleImageSelect}
                />
              </motion.div>
            ) : (
              /* Preview & Action State */
              <motion.div
                key="preview"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="bg-surface rounded-4xl p-6 shadow-soft border border-primary/10 space-y-6"
              >
                <div className="relative rounded-3xl overflow-hidden bg-muted aspect-[4/3] flex items-center justify-center">
                  <img 
                    src={previewUrl} 
                    alt="Hieroglyph Preview" 
                    className="w-full h-full object-contain"
                  />
                  {!isLoading && !result && (
                    <button 
                      onClick={handleReset}
                      className="absolute top-4 right-4 bg-black/50 hover:bg-black/70 backdrop-blur-md text-white p-2 rounded-full transition-colors"
                    >
                      <RefreshCw className="w-5 h-5" />
                    </button>
                  )}
                </div>

                {!result && !isLoading && (
                  <button 
                    onClick={handleTranslate}
                    className="w-full py-4 px-6 bg-primary text-primary-foreground rounded-full font-rounded font-semibold text-lg shadow-lg hover:shadow-xl hover:scale-[1.02] transition-all duration-300 flex items-center justify-center gap-2"
                  >
                    Translate Hieroglyph <ArrowRight className="w-5 h-5" />
                  </button>
                )}

                {isLoading && (
                  <div className="py-8 flex flex-col items-center justify-center space-y-4">
                    <motion.div 
                      animate={{ rotate: 360 }}
                      transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
                      className="w-12 h-12 border-4 border-primary/20 border-t-primary rounded-full"
                    />
                    <p className="text-primary font-medium font-rounded animate-pulse">Consulting the ancient scribes...</p>
                  </div>
                )}

                {error && (
                  <div className="p-4 bg-red-50 text-red-600 rounded-2xl flex items-start gap-3">
                    <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
                    <p className="text-sm font-medium">{error}</p>
                  </div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Results Section */}
        <AnimatePresence>
          {result && (
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="space-y-6"
            >
              <div className="flex items-center justify-between px-2">
                <h2 className="text-2xl font-rounded font-bold text-foreground">Translation Discovered</h2>
                <button 
                  onClick={handleReset}
                  className="text-primary font-medium text-sm hover:underline"
                >
                  Start Over
                </button>
              </div>

              <div className="grid gap-6">
                {/* Summary */}
                <motion.div 
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.3 }}
                  className="bg-surface p-6 rounded-3xl shadow-soft border border-primary/10 relative overflow-hidden"
                >
                  <div className="absolute top-0 right-0 w-24 h-24 bg-primary/5 rounded-bl-full -mr-4 -mt-4"></div>
                  <div className="flex items-center gap-3 mb-3 text-primary">
                    <ScrollText className="w-5 h-5" />
                    <h3 className="font-rounded font-semibold text-lg">Modern Summary</h3>
                  </div>
                  <p className="text-foreground text-lg leading-relaxed">{result.summary}</p>
                </motion.div>

                {/* Historical Insight */}
                <motion.div 
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.5 }}
                  className="bg-surface p-6 rounded-3xl shadow-soft border border-primary/10 relative overflow-hidden"
                >
                  <div className="absolute top-0 right-0 w-24 h-24 bg-primary/5 rounded-bl-full -mr-4 -mt-4"></div>
                  <div className="flex items-center gap-3 mb-3 text-primary">
                    <Landmark className="w-5 h-5" />
                    <h3 className="font-rounded font-semibold text-lg">Historical Insight</h3>
                  </div>
                  <p className="text-muted-foreground leading-relaxed">{result.historical_insight}</p>
                </motion.div>

                {/* Literal Translation */}
                <motion.div 
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.7 }}
                  className="bg-surface p-6 rounded-3xl shadow-soft border border-primary/10 relative overflow-hidden"
                >
                  <div className="absolute top-0 right-0 w-24 h-24 bg-primary/5 rounded-bl-full -mr-4 -mt-4"></div>
                  <div className="flex items-center gap-3 mb-3 text-primary">
                    <BookOpen className="w-5 h-5" />
                    <h3 className="font-rounded font-semibold text-lg">Literal Translation</h3>
                  </div>
                  <p className="text-foreground text-lg leading-relaxed">{result.literal_translation}</p>
                </motion.div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

      </main>
    </div>
  );
}
