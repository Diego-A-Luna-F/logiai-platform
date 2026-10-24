import { useState } from 'react'
import Navbar from './components/Navbar'
import FileUpload from './components/FileUpload'
import AnalysisViewer from './components/AnalysisViewer'

function App() {
  const [currentAnalysis, setCurrentAnalysis] = useState(null)

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Navbar />
      
      <main className="flex-1 max-w-7xl w-full mx-auto px-6 py-8 grid grid-cols-1 lg:grid-cols-12 gap-8">
        <section className="lg:col-span-5 space-y-6">
          <FileUpload onUploadSuccess={(data) => setCurrentAnalysis(data)} />
        </section>
        
        <section className="lg:col-span-7">
          <AnalysisViewer analysisData={currentAnalysis} />
        </section>
      </main>
    </div>
  )
}

export default App