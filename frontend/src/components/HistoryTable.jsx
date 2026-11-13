import { useState, useEffect } from 'react'

export default function HistoryTable({ refreshTrigger, onViewDetails }) {
  const [documents, setDocuments] = useState([])
  const [loading, setLoading] = useState(true)
  
  const [searchTerm, setSearchTerm] = useState('')
  const [riskFilter, setRiskFilter] = useState('')

  useEffect(() => {
    const fetchHistory = async () => {
      setLoading(true)
      try {
        const queryParams = new URLSearchParams()
        if (searchTerm) queryParams.append('search', searchTerm)
        if (riskFilter) queryParams.append('risk_level', riskFilter)
        
        const url = `http://localhost:8000/api/v1/documents/?${queryParams.toString()}`
        
        const response = await fetch(url)
        if (!response.ok) throw new Error('Error al cargar el historial')
        
        const data = await response.json()
        setDocuments(Array.isArray(data) ? data : [])
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    const delayDebounceFn = setTimeout(() => {
      fetchHistory()
    }, 300)

    return () => clearTimeout(delayDebounceFn)
  }, [refreshTrigger, searchTerm, riskFilter])

  // Lógica para asignar colores dinámicos al select según el valor escogido
  const selectColorClass = 
    riskFilter === 'Alto' ? 'text-red-400 border-red-500/30 bg-red-500/10' :
    riskFilter === 'Medio' ? 'text-amber-400 border-amber-500/30 bg-amber-500/10' :
    riskFilter === 'Bajo' ? 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10' :
    'text-slate-300 border-slate-700 bg-slate-900/50'

  return (
    <div className="bg-slate-800/50 border border-slate-700/60 rounded-2xl p-6 shadow-xl mt-6 space-y-4">
      
      <div className="flex flex-col gap-4 border-b border-slate-700/60 pb-4">
        <h2 className="text-lg font-semibold text-white">Historial de Análisis</h2>
        
        <div className="flex flex-col sm:flex-row w-full gap-3">
          <div className="relative flex-1">
            <svg className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input 
              type="text" 
              placeholder="Buscar documento..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-9 pr-4 py-1.5 bg-slate-900/50 border border-slate-700 text-sm text-white rounded-lg focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 w-full transition-all"
            />
          </div>

          <select 
            value={riskFilter}
            onChange={(e) => setRiskFilter(e.target.value)}
            className={`px-3 py-1.5 border text-sm rounded-lg focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 w-full sm:w-auto cursor-pointer transition-colors ${selectColorClass}`}
          >
            <option value="" className="text-slate-300 bg-slate-900">Todos los riesgos</option>
            <option value="Alto" className="text-red-400 bg-slate-900">Riesgo Alto</option>
            <option value="Medio" className="text-amber-400 bg-slate-900">Riesgo Medio</option>
            <option value="Bajo" className="text-emerald-400 bg-slate-900">Riesgo Bajo</option>
          </select>
        </div>
      </div>
      
      {loading && documents.length === 0 ? (
        <div className="text-center text-slate-400 text-sm py-8 animate-pulse">
          Buscando en la base de datos...
        </div>
      ) : (
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
                    No se encontraron documentos.
                  </td>
                </tr>
              ) : (
                documents.map((doc) => {
                  const risk = doc.risk_level
                  
                  const riskColor = 
                    risk === 'Alto' ? 'bg-red-500/10 text-red-400 border-red-500/20' :
                    risk === 'Medio' ? 'bg-amber-500/10 text-amber-400 border-amber-500/20' :
                    risk === 'Bajo' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
                    'bg-slate-500/10 text-slate-400 border-slate-500/20'

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
      )}
    </div>
  )
}