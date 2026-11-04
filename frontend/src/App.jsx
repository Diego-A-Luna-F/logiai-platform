import { useState } from 'react'
import Navbar from './components/Navbar'
import FileUpload from './components/FileUpload'
import AnalysisViewer from './components/AnalysisViewer'
import HistoryTable from './components/HistoryTable'

function App() {
  const [currentAnalysis, setCurrentAnalysis] = useState(null)
  const [refreshKey, setRefreshKey] = useState(0)

  const handleUploadSuccess = (data) => {
    setCurrentAnalysis(data)
    setRefreshKey(prev => prev + 1) // Cambia el número y fuerza la recarga de HistoryTable
  }

  const handleViewDetails = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/documents/${id}`)
      if (!response.ok) throw new Error('Error al obtener los detalles del documento')
      
      const data = await response.json()

      // Normalizamos los nombres de las llaves de la DB SQL que espera AnalysisViewer
      const normalizedData = {
        filename: data.filename,
        ai_analysis: {
          risk_level: data.analysis.risk_level,
          summary: data.analysis.summary,
          anomalies_detected: data.analysis.anomalies, // DB usa "anomalies"
          items: data.analysis.items_detected // DB usa "items_detected"
        }
      }

      setCurrentAnalysis(normalizedData)
    } catch (error) {
      console.error(error)
      // Opcional: Aquí podrías agregar un estado para mostrar un Toast de error
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Navbar />
      
      <main className="flex-1 max-w-7xl w-full mx-auto px-6 py-8 grid grid-cols-1 lg:grid-cols-12 gap-8">
        <section className="lg:col-span-5 space-y-6">
          <FileUpload onUploadSuccess={handleUploadSuccess} />
          <HistoryTable refreshTrigger={refreshKey} onViewDetails={handleViewDetails} />
        </section>
        
        <section className="lg:col-span-7">
          <AnalysisViewer analysisData={currentAnalysis} />
        </section>
      </main>
    </div>
  )
}

export default App