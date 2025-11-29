import { useWallet } from './hooks/useWallet';

function App() {
  const { address, isConnected, connect } = useWallet();

  return (
    <div className='min-h-screen bg-dark text-white font-sans selection:bg-primary/30'>
      <nav className='flex items-center justify-between px-8 py-6 border-b border-white/5 backdrop-blur-md fixed w-full z-50 bg-dark/80'>
        <div className='flex items-center gap-3'>
          <div className='relative'>
            <div className='w-10 h-10 rounded-full bg-gradient-to-tr from-accent via-secondary to-primary p-[2px]'>
              <div className='w-full h-full rounded-full bg-dark flex items-center justify-center'>
                <span className='text-xl'>🛒</span>
              </div>
            </div>
            <div className='absolute -top-1 -right-1 w-3 h-3 bg-primary rounded-full animate-pulse shadow-[0_0_10px_#31DBC3]'></div>
          </div>
          <div className='flex flex-col'>
            <span className='text-xl font-heading font-bold tracking-tight'>Agilize.ai</span>
            <span className='text-[10px] text-slate-400 uppercase tracking-widest'>Powered by GuardFlow</span>
          </div>
        </div>
        
        <div className='hidden md:flex gap-8 text-sm font-medium text-slate-300'>
          <a href='#' className='hover:text-primary transition-colors'>Soluções</a>
          <a href='#' className='hover:text-primary transition-colors'>Para Varejo</a>
          <a href='#' className='hover:text-primary transition-colors'>Sustentabilidade</a>
        </div>

        <button 
          onClick={connect}
          className={`px-5 py-2.5 rounded-full font-medium transition-all duration-300 ${
            isConnected 
              ? 'bg-primary/10 text-primary border border-primary/20' 
              : 'bg-gradient-to-r from-primary to-secondary text-dark hover:shadow-[0_0_20px_rgba(49,219,195,0.3)] hover:scale-105'
          }`}
        >
          {isConnected ? `${address?.slice(0, 6)}...${address?.slice(-4)}` : 'Conectar Carteira'}
        </button>
      </nav>

      <main className='pt-32 pb-16 px-8 max-w-7xl mx-auto'>
        <div className='grid grid-cols-1 lg:grid-cols-2 gap-20 items-center min-h-[60vh]'>
          <div className='space-y-8'>
            <div className='inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 backdrop-blur-sm'>
              <span className='w-2 h-2 rounded-full bg-primary animate-pulse'></span>
              <span className='text-sm text-slate-300'>Tecnologia Ética para o Varejo</span>
            </div>
            
            <h1 className='text-6xl font-heading font-bold leading-tight'>
              Menos fila.<br/>
              <span className='text-transparent bg-clip-text bg-gradient-to-r from-accent via-secondary to-primary'>
                Mais vida.
              </span>
            </h1>
            
            <p className='text-xl text-slate-400 leading-relaxed max-w-lg'>
              A Agilize.ai une inteligência artificial e empatia para transformar a experiência de compra. Sem filas, sem atrito, com total transparência.
            </p>

            <div className='flex flex-col sm:flex-row gap-4'>
              <button className='px-8 py-4 bg-primary text-dark font-bold rounded-xl hover:bg-primary/90 transition-all shadow-[0_0_30px_rgba(49,219,195,0.2)] flex items-center justify-center gap-2'>
                <span>Experimentar Agora</span>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
              </button>
              <button className='px-8 py-4 border border-white/10 text-white rounded-xl hover:bg-white/5 transition-all flex items-center justify-center gap-2'>
                <span>Ver Demonstração</span>
                <span className="text-xs bg-white/10 px-2 py-1 rounded text-slate-300">v1.0</span>
              </button>
            </div>

            <div className='pt-8 border-t border-white/5 flex gap-8'>
              <div>
                <p className='text-3xl font-bold text-white'>-45%</p>
                <p className='text-sm text-slate-400'>Tempo em filas</p>
              </div>
              <div>
                <p className='text-3xl font-bold text-white'>100%</p>
                <p className='text-sm text-slate-400'>Auditado por IA</p>
              </div>
              <div>
                <p className='text-3xl font-bold text-white'>ESG</p>
                <p className='text-sm text-slate-400'>Score Verificado</p>
              </div>
            </div>
          </div>

          <div className='relative'>
            <div className='absolute -inset-4 bg-gradient-to-tr from-accent via-secondary to-primary rounded-[2rem] blur-2xl opacity-20 animate-pulse'></div>
            <div className='relative bg-dark/80 backdrop-blur-xl border border-white/10 rounded-[2rem] p-8 shadow-2xl'>
              <div className='flex items-center justify-between mb-8'>
                <div className='flex items-center gap-3'>
                  <div className='w-10 h-10 rounded-full bg-white/5 flex items-center justify-center'>👤</div>
                  <div>
                    <h3 className='font-bold'>João Silva</h3>
                    <p className='text-xs text-primary'>Cliente Verificado</p>
                  </div>
                </div>
                <span className='text-2xl font-bold text-primary'>98/100</span>
              </div>
              
              <div className='space-y-4'>
                <div className='p-4 bg-white/5 rounded-xl border border-white/5 hover:border-primary/30 transition-colors cursor-pointer group'>
                  <div className='flex justify-between items-center mb-2'>
                    <span className='text-sm font-medium text-slate-300 group-hover:text-white'>Carrinho Inteligente</span>
                    <span className='text-xs bg-primary/20 text-primary px-2 py-1 rounded-full'>Ativo</span>
                  </div>
                  <div className='w-full bg-white/10 h-1.5 rounded-full overflow-hidden'>
                    <div className='bg-primary h-full w-[85%]'></div>
                  </div>
                </div>

                <div className='p-4 bg-white/5 rounded-xl border border-white/5 hover:border-secondary/30 transition-colors cursor-pointer group'>
                  <div className='flex justify-between items-center mb-2'>
                    <span className='text-sm font-medium text-slate-300 group-hover:text-white'>Pegada de Carbono</span>
                    <span className='text-xs bg-secondary/20 text-secondary px-2 py-1 rounded-full'>Neutro</span>
                  </div>
                  <div className='w-full bg-white/10 h-1.5 rounded-full overflow-hidden'>
                    <div className='bg-secondary h-full w-[92%]'></div>
                  </div>
                </div>

                <div className='p-4 bg-white/5 rounded-xl border border-white/5 hover:border-accent/30 transition-colors cursor-pointer group'>
                  <div className='flex justify-between items-center mb-2'>
                    <span className='text-sm font-medium text-slate-300 group-hover:text-white'>Privacidade de Dados</span>
                    <span className='text-xs bg-accent/20 text-accent px-2 py-1 rounded-full'>Protegido</span>
                  </div>
                  <div className='w-full bg-white/10 h-1.5 rounded-full overflow-hidden'>
                    <div className='bg-accent h-full w-[100%]'></div>
                  </div>
                </div>
              </div>

              <div className='mt-8 pt-6 border-t border-white/5 text-center'>
                <p className='text-xs text-slate-500 uppercase tracking-widest mb-2'>Powered by</p>
                <span className='text-lg font-bold tracking-tight text-white/80'>GuardFlow Protocol</span>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
