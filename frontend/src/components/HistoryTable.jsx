import { useState, useEffect } from 'react'

export default function HistoryTable({ refreshTrigger, onViewDetails }) {
  const [documents, setDocuments] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/documents/')
        if (!response.ok) throw new Error('Error al cargar el historial')
        
        const data = await response.json()
        setDocuments(Array.isArray(data) ? data.reverse() : [])
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchHistory()
  }, [refreshTrigger]) // Se vuelve a ejecutar cuando refreshTrigger cambia

  if (loading) {
    return (
      <div className="bg-slate-800/50 border border-slate-700/60 rounded-2xl p-6 shadow-xl mt-6 text-center text-slate-400 text-sm animate-pulse">
        Cargando historial de la base de datos...
      </div>
    )
  }

  return (
    <div className="bg-slate-800/50 border border-slate-700/60 rounded-2xl p-6 shadow-xl mt-6">
      <h2 className="text-lg font-semibold text-white mb-4">Historial de Análisis</h2>
      
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm text-slate-400">
          <thead className="text-xs uppercase bg-slate-900/60 text-slate-300">
            <tr>
              <th className="px-4 py-3 rounded-tl-lg">Documento</th>
              <th className="px-4 py-3">Riesgo</th>
              <th className="px-4 py-3 rounded-tr-lg">Estado</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700/50">
            {documents.length === 0 ? (
              <tr>
                <td colSpan="3" className="px-4 py-6 text-center text-slate-500 italic">
                  No hay documentos almacenados en SQLite.
                </td>
              </tr>
            ) : (
              documents.map((doc) => {
                const risk = doc.risk_level
                
                const riskColor = 
                  risk === 'Alto' ? 'bg-red-500/10 text-red-400 border-red-500/20' :
                  risk === 'Medio' ? 'bg-amber-500/10 text-amber-400 border-amber-500/20' :
                  risk === 'N/A' ? 'bg-slate-500/10 text-slate-400 border-slate-500/20' :
                  'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'

                return (
                  <tr
                    key={doc.id} 
                    onClick={() => onViewDetails(doc.id)}
                    className="hover:bg-slate-700/40 transition-colors cursor-pointer"
                  >
                    <td className="px-4 py-3 font-medium text-slate-200 truncate max-w-[150px]" title={doc.filename}>
                      {doc.filename}
                    </td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 rounded text-xs font-semibold border ${riskColor}`}>
                        {risk}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <span className="px-2 py-1 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 text-xs">
                        {doc.status || 'Procesado'}
                      </span>
                    </td>
                  </tr>
                )
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}