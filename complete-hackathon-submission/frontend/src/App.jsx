import React, { useState } from 'react';
import { Upload, FileAudio, Loader2, CheckCircle2, XCircle, AlertCircle } from 'lucide-react';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Your deployed API URL - UPDATE THIS AFTER DEPLOYING TO RENDER
  const API_URL = 'https://your-api-name.onrender.com/api/call-analytics';
  const API_KEY = 'sk_track3_987654321';

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'audio/mpeg') {
      setFile(selectedFile);
      setError(null);
      setResult(null);
    } else {
      setError('Please select a valid MP3 file');
      setFile(null);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type === 'audio/mpeg') {
      setFile(droppedFile);
      setError(null);
      setResult(null);
    } else {
      setError('Please drop a valid MP3 file');
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const analyzeAudio = async () => {
    if (!file) {
      setError('Please select an audio file first');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Convert file to Base64
      const reader = new FileReader();
      reader.readAsDataURL(file);
      
      reader.onload = async () => {
        const base64Audio = reader.result.split(',')[1];

        // Call API
        const response = await fetch(API_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'x-api-key': API_KEY,
          },
          body: JSON.stringify({
            language: 'Tamil',
            audioFormat: 'mp3',
            audioBase64: base64Audio,
          }),
        });

        if (!response.ok) {
          throw new Error(`API Error: ${response.status}`);
        }

        const data = await response.json();
        setResult(data);
        setLoading(false);
      };

      reader.onerror = () => {
        setError('Error reading file');
        setLoading(false);
      };
    } catch (err) {
      setError(err.message || 'Failed to analyze audio. Please try again.');
      setLoading(false);
    }
  };

  const getComplianceColor = (score) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getComplianceLabel = (score) => {
    if (score >= 0.8) return 'Excellent';
    if (score >= 0.6) return 'Good';
    if (score >= 0.4) return 'Fair';
    return 'Poor';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Call Center Compliance Analyzer
              </h1>
              <p className="mt-1 text-sm text-gray-500">
                AI-Powered SOP Validation & Analytics
              </p>
            </div>
            <div className="hidden sm:block">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                GUVI Hackathon 2026
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Upload Section */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">
            Upload Call Recording
          </h2>
          
          {/* Drag & Drop Area */}
          <div
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-blue-500 transition-colors cursor-pointer"
          >
            <input
              type="file"
              accept="audio/mpeg"
              onChange={handleFileChange}
              className="hidden"
              id="file-upload"
            />
            <label htmlFor="file-upload" className="cursor-pointer">
              <Upload className="mx-auto h-12 w-12 text-gray-400" />
              <p className="mt-4 text-lg text-gray-600">
                {file ? (
                  <span className="flex items-center justify-center gap-2">
                    <FileAudio className="h-5 w-5 text-blue-600" />
                    <span className="font-medium text-blue-600">{file.name}</span>
                  </span>
                ) : (
                  <>
                    <span className="font-semibold text-blue-600">Click to upload</span> or drag and drop
                  </>
                )}
              </p>
              <p className="mt-2 text-sm text-gray-500">MP3 audio files only</p>
            </label>
          </div>

          {/* Analyze Button */}
          <div className="mt-6">
            <button
              onClick={analyzeAudio}
              disabled={!file || loading}
              className="w-full sm:w-auto px-8 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="h-5 w-5 animate-spin" />
                  Analyzing... (15-30 seconds)
                </>
              ) : (
                'Analyze Call Recording'
              )}
            </button>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
              <AlertCircle className="h-5 w-5 text-red-600 mt-0.5" />
              <p className="text-red-800">{error}</p>
            </div>
          )}
        </div>

        {/* Results Section */}
        {result && (
          <div className="space-y-6">
            {/* Summary Card */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Summary</h3>
              <p className="text-gray-700 leading-relaxed">{result.summary}</p>
            </div>

            {/* SOP Validation */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-6">SOP Compliance</h3>
              
              {/* Compliance Score */}
              <div className="mb-6 p-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Compliance Score</p>
                    <p className={`text-4xl font-bold ${getComplianceColor(result.sop_validation.complianceScore)}`}>
                      {(result.sop_validation.complianceScore * 100).toFixed(0)}%
                    </p>
                    <p className="text-sm mt-1 text-gray-600">
                      {getComplianceLabel(result.sop_validation.complianceScore)}
                    </p>
                  </div>
                  <div className="text-right">
                    <span className={`inline-flex items-center px-4 py-2 rounded-full text-sm font-medium ${
                      result.sop_validation.adherenceStatus === 'FOLLOWED'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {result.sop_validation.adherenceStatus}
                    </span>
                  </div>
                </div>
              </div>

              {/* SOP Steps */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-6">
                {[
                  { key: 'greeting', label: 'Greeting' },
                  { key: 'identification', label: 'Identification' },
                  { key: 'problemStatement', label: 'Problem' },
                  { key: 'solutionOffering', label: 'Solution' },
                  { key: 'closing', label: 'Closing' },
                ].map((step) => (
                  <div key={step.key} className="p-4 bg-gray-50 rounded-lg text-center">
                    {result.sop_validation[step.key] ? (
                      <CheckCircle2 className="h-8 w-8 text-green-600 mx-auto mb-2" />
                    ) : (
                      <XCircle className="h-8 w-8 text-red-600 mx-auto mb-2" />
                    )}
                    <p className="text-sm font-medium text-gray-900">{step.label}</p>
                    <p className={`text-xs mt-1 ${
                      result.sop_validation[step.key] ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {result.sop_validation[step.key] ? 'Complete' : 'Missing'}
                    </p>
                  </div>
                ))}
              </div>

              {/* Explanation */}
              <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-sm font-medium text-blue-900 mb-1">Analysis</p>
                <p className="text-sm text-blue-800">{result.sop_validation.explanation}</p>
              </div>
            </div>

            {/* Analytics */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Payment Preference */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h4 className="text-lg font-semibold text-gray-900 mb-4">Payment Preference</h4>
                <div className="flex items-center justify-center h-24">
                  <span className="inline-flex items-center px-4 py-2 rounded-lg text-lg font-medium bg-blue-100 text-blue-800">
                    {result.analytics.paymentPreference}
                  </span>
                </div>
              </div>

              {/* Rejection Reason */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h4 className="text-lg font-semibold text-gray-900 mb-4">Rejection Reason</h4>
                <div className="flex items-center justify-center h-24">
                  <span className={`inline-flex items-center px-4 py-2 rounded-lg text-lg font-medium ${
                    result.analytics.rejectionReason === 'NONE'
                      ? 'bg-green-100 text-green-800'
                      : 'bg-orange-100 text-orange-800'
                  }`}>
                    {result.analytics.rejectionReason}
                  </span>
                </div>
              </div>

              {/* Sentiment */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h4 className="text-lg font-semibold text-gray-900 mb-4">Customer Sentiment</h4>
                <div className="flex items-center justify-center h-24">
                  <span className={`inline-flex items-center px-4 py-2 rounded-lg text-lg font-medium ${
                    result.analytics.sentiment === 'Positive'
                      ? 'bg-green-100 text-green-800'
                      : result.analytics.sentiment === 'Negative'
                      ? 'bg-red-100 text-red-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}>
                    {result.analytics.sentiment}
                  </span>
                </div>
              </div>
            </div>

            {/* Keywords */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Keywords</h3>
              <div className="flex flex-wrap gap-2">
                {result.keywords.map((keyword, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800"
                  >
                    {keyword}
                  </span>
                ))}
              </div>
            </div>

            {/* Transcript */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Full Transcript</h3>
              <div className="bg-gray-50 rounded-lg p-4 max-h-96 overflow-y-auto">
                <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">
                  {result.transcript}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Info Section */}
        {!result && !loading && (
          <div className="bg-white rounded-xl shadow-lg p-8">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">How It Works</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="bg-blue-100 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
                  <span className="text-blue-600 font-bold text-xl">1</span>
                </div>
                <h4 className="font-medium text-gray-900 mb-2">Upload Audio</h4>
                <p className="text-sm text-gray-600">
                  Upload your MP3 call recording (Tamil/Hindi supported)
                </p>
              </div>
              <div className="text-center">
                <div className="bg-purple-100 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
                  <span className="text-purple-600 font-bold text-xl">2</span>
                </div>
                <h4 className="font-medium text-gray-900 mb-2">AI Analysis</h4>
                <p className="text-sm text-gray-600">
                  Groq Whisper transcribes, Gemini AI analyzes compliance
                </p>
              </div>
              <div className="text-center">
                <div className="bg-green-100 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
                  <span className="text-green-600 font-bold text-xl">3</span>
                </div>
                <h4 className="font-medium text-gray-900 mb-2">Get Insights</h4>
                <p className="text-sm text-gray-600">
                  View SOP compliance, sentiment, and business intelligence
                </p>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-500">
            Built for GUVI Hackathon 2026 | Powered by Groq Whisper & Google Gemini
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
