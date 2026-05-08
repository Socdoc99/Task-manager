import { useState } from 'react'

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-3xl shadow-2xl overflow-hidden transform transition-all hover:scale-[1.02]">
        <div className="p-8">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
                Task Manager
              </h1>
              <p className="text-slate-500 mt-1 font-medium">Fase 4: Frontend React</p>
            </div>
            <span className="bg-indigo-100 text-indigo-700 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">
              En línea
            </span>
          </div>

          <div className="mt-8 space-y-4">
            <div className="p-4 bg-slate-50 rounded-xl border border-slate-100 flex items-center gap-4">
              <div className="h-10 w-10 bg-indigo-600 rounded-lg flex items-center justify-center text-white shadow-lg">
                🚀
              </div>
              <div>
                <h3 className="font-bold text-slate-800">Tailwind CSS v4</h3>
                <p className="text-sm text-slate-500">Configuración completada</p>
              </div>
            </div>
          </div>

          <button className="w-full mt-8 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-4 rounded-2xl shadow-lg shadow-indigo-200 transition-all active:transform active:scale-95">
            Comenzar Proyecto
          </button>
        </div>
      </div>
    </div>
  )
}

export default App