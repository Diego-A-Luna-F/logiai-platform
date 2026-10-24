export default function AnalysisViewer({ analysisData }) {
  if (!analysisData) {
    return (
      <div className="bg-slate-800/30 border border-slate-700/40 rounded-2xl p-8 text-center text-slate-500">
        Suba un manifiesto para desplegar el análisis generado por IA.
      </div>
    )
  }

  const { filename, ai_analysis } = analysisData
  const riskColor = 
    ai_analysis?.risk_level === 'Alto' ? 'bg-red-500/10 text-red-400 border-red-500/30' :
    ai_analysis?.risk_level === 'Medio' ? 'bg-amber-500/10 text-amber-400 border-amber-500/30' :
    'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'

  return (
    <div className="bg-slate-800/50 border border-slate-700/60 rounded-2xl p-6 shadow-xl space-y-6">
      <div className="flex justify-between items-start border-b border-slate-700/60 pb-4">
        <div>
          <span className="text-xs font-mono text-blue-400 uppercase tracking-wider">Documento Analizado</span>
          <h2 className="text-xl font-bold text-white mt-1">{filename}</h2>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${riskColor}`}>
          Riesgo: {ai_analysis?.risk_level || 'Evaluando'}
        </span>
      </div>

      <div>
        <h3 className="text-sm font-semibold text-slate-300 mb-2">Resumen Ejecutivo</h3>
        <p className="text-slate-400 text-sm leading-relaxed">{ai_analysis?.summary}</p>
      </div>

      {ai_analysis?.anomalies_detected?.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-amber-400 mb-2">Anomalías Detectadas</h3>
          <ul className="list-disc list-inside text-sm text-slate-400 space-y-1">
            {ai_analysis.anomalies_detected.map((item, idx) => (
              <li key={idx} className="text-amber-300/90">{item}</li>
            ))}
          </ul>
        </div>
      )}

      {ai_analysis?.items?.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-slate-300 mb-3">Ítems Procesados</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-400">
              <thead className="text-xs uppercase bg-slate-900/60 text-slate-300">
                <tr>
                  <th className="px-4 py-3">SKU</th>
                  <th className="px-4 py-3">Descripción</th>
                  <th className="px-4 py-3">Cantidad</th>
                  <th className="px-4 py-3">Estado</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-700/50">
                {ai_analysis.items.map((item, idx) => (
                  <tr key={idx} className="hover:bg-slate-700/20">
                    <td className="px-4 py-3 font-mono text-blue-300">{item.sku}</td>
                    <td className="px-4 py-3 text-slate-200">{item.description}</td>
                    <td className="px-4 py-3">{item.quantity}</td>
                    <td className="px-4 py-3">{item.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}