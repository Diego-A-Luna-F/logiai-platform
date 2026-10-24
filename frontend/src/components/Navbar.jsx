export default function Navbar() {
  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center font-bold text-white shadow-lg shadow-blue-500/20">
            L
          </div>
          <div>
            <h1 className="text-lg font-bold text-white tracking-wide">LogiAI</h1>
            <p className="text-xs text-slate-400">Platform & Analytics</p>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
          <span className="text-xs text-slate-300 font-medium">API Conectada</span>
        </div>
      </div>
    </header>
  )
}