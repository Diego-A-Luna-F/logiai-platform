import { useState } from 'react'

export default function FileUpload({ onUploadSuccess }) {
  const [isHovering, setIsHovering] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleFileChange = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    setLoading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://localhost:8000/api/v1/documents/upload', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) throw new Error('Error al analizar el archivo')

      const data = await response.json()
      onUploadSuccess(data)
    } catch (err) {
      alert(`Error: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-slate-800/50 border border-slate-700/60 rounded-2xl p-6 shadow-xl">
      <h2 className="text-lg font-semibold text-white mb-4">Subir Documento Logístico</h2>
      
      <label
        onDragOver={(e) => { e.preventDefault(); setIsHovering(true) }}
        onDragLeave={() => setIsHovering(false)}
        onDrop={(e) => {
          e.preventDefault()
          setIsHovering(false)
          if (e.dataTransfer.files?.[0]) {
            handleFileChange({ target: { files: e.dataTransfer.files } })
          }
        }}
        className={`flex flex-col items-center justify-center w-full h-48 border-2 border-dashed rounded-xl cursor-pointer transition-all duration-200 ${
          isHovering
            ? 'border-blue-500 bg-blue-500/10'
            : 'border-slate-600 hover:border-slate-500 bg-slate-900/40'
        }`}
      >
        <div className="flex flex-col items-center justify-center pt-5 pb-6 text-center px-4">
          <svg className="w-10 h-10 mb-3 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
          <p className="mb-1 text-sm text-slate-300 font-medium">
            {loading ? 'Procesando con Gemini AI...' : 'Haz clic o arrastra un manifiesto aquí'}
          </p>
          <p className="text-xs text-slate-500">PDF o TXT (Formatos soportados)</p>
        </div>
        <input type="file" className="hidden" onChange={handleFileChange} accept=".pdf,.txt" disabled={loading} />
      </label>
    </div>
  )
}