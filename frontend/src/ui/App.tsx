import React, { useState } from 'react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'
import logo from './logo-sort.svg'

const App: React.FC = () => {
  const [prompt, setPrompt] = useState('Create a Python script that prints Fibonacci numbers up to 100.')
  const [repoOwner, setRepoOwner] = useState('')
  const [repoName, setRepoName] = useState('sort-generated-repo')
  const [githubExport, setGithubExport] = useState(true)
  const [createDocker, setCreateDocker] = useState(false)
  const [imageName, setImageName] = useState('')
  const [deployNetlify, setDeployNetlify] = useState(false)
  const [netlifyBuildCmd, setNetlifyBuildCmd] = useState('npm run build')
  const [netlifyPublishDir, setNetlifyPublishDir] = useState('dist')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const runPipeline = async () => {
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const res = await axios.post('/api/run-pipeline/', {
        prompt,
        repo_owner: repoOwner,
        repo_name: repoName,
        github_export: githubExport,
        create_docker: createDocker,
        image_name: imageName || undefined,
        deploy_netlify: deployNetlify,
        netlify_build_cmd: netlifyBuildCmd,
        netlify_publish_dir: netlifyPublishDir,
      })
      setResult(res.data)
    } catch (e: any) {
      setError(e?.response?.data?.error || e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{minHeight: '100vh', background: 'linear-gradient(135deg, #1a1a2e 0%, #23234b 100%)', color: '#fff', fontFamily: 'Inter, system-ui, sans-serif', padding: 0, margin: 0}}>
      <div style={{maxWidth: 540, margin: '48px auto', background: 'rgba(24,24,32,0.98)', borderRadius: 22, boxShadow: '0 8px 40px #000a', padding: '44px 40px 36px 40px', border: '1.5px solid #23234b'}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 18, marginBottom: 28}}>
          <img src={logo} alt="SORT Logo" style={{width: 54, height: 54, borderRadius: 14, background: '#222', boxShadow: '0 2px 8px #0004'}} />
          <h1 style={{fontWeight: 900, fontSize: 32, letterSpacing: -1.5, margin: 0, color: '#fff', textShadow: '0 2px 8px #0006'}}>SORT Orchestrator</h1>
        </div>
        <p style={{color: '#b3b3e6', fontSize: 16, marginBottom: 32, lineHeight: 1.6}}>Authenticate with GitHub (OAuth), then run your DevOps pipeline.<br/>All actions are performed securely on your account.</p>

        <div style={{marginBottom: 24}}>
          <label style={{fontWeight: 700, color: '#fff', fontSize: 16}}>Prompt</label>
          <textarea value={prompt} onChange={e => setPrompt(e.target.value)} rows={4} style={{width: '100%', background: '#23234b', color: '#fff', border: '1.5px solid #333', borderRadius: 10, padding: 12, fontSize: 16, marginTop: 8, resize: 'vertical', boxShadow: '0 1px 4px #0002'}}/>
        </div>

        <div style={{display: 'flex', gap: 14, marginBottom: 20}}>
          <div style={{flex: 1}}>
            <label style={{fontWeight: 700, color: '#fff'}}>Repo Owner</label>
            <input value={repoOwner} onChange={e => setRepoOwner(e.target.value)} style={{width: '100%', background: '#23234b', color: '#fff', border: '1.5px solid #333', borderRadius: 10, padding: 10, fontSize: 15, marginTop: 8}} />
          </div>
          <div style={{flex: 1}}>
            <label style={{fontWeight: 700, color: '#fff'}}>Repo Name</label>
            <input value={repoName} onChange={e => setRepoName(e.target.value)} style={{width: '100%', background: '#23234b', color: '#fff', border: '1.5px solid #333', borderRadius: 10, padding: 10, fontSize: 15, marginTop: 8}} />
          </div>
        </div>

        <div style={{display: 'flex', gap: 14, marginBottom: 20}}>
          <label style={{display: 'flex', alignItems: 'center', gap: 8, fontWeight: 600, fontSize: 15}}>
            <input type="checkbox" checked={githubExport} onChange={e => setGithubExport(e.target.checked)} style={{accentColor: '#6c63ff'}} />
            Export to GitHub
          </label>
          <label style={{display: 'flex', alignItems: 'center', gap: 8, fontWeight: 600, fontSize: 15}}>
            <input type="checkbox" checked={createDocker} onChange={e => setCreateDocker(e.target.checked)} style={{accentColor: '#6c63ff'}} />
            Create Docker (GHCR workflow)
          </label>
        </div>
        {createDocker && (
          <input placeholder="Image name (optional)" value={imageName} onChange={e => setImageName(e.target.value)} style={{width: '100%', background: '#23234b', color: '#fff', border: '1.5px solid #333', borderRadius: 10, padding: 10, fontSize: 15, marginBottom: 20}} />
        )}

        <div style={{marginBottom: 20}}>
          <label style={{display: 'flex', alignItems: 'center', gap: 8, fontWeight: 600, fontSize: 15}}>
            <input type="checkbox" checked={deployNetlify} onChange={e => setDeployNetlify(e.target.checked)} style={{accentColor: '#6c63ff'}} />
            Add Netlify config
          </label>
          {deployNetlify && (
            <div style={{display: 'flex', gap: 14, marginTop: 10}}>
              <div style={{flex: 1}}>
                <label style={{fontWeight: 700, color: '#fff'}}>Build command</label>
                <input value={netlifyBuildCmd} onChange={e => setNetlifyBuildCmd(e.target.value)} style={{width: '100%', background: '#23234b', color: '#fff', border: '1.5px solid #333', borderRadius: 10, padding: 10, fontSize: 15, marginTop: 8}} />
              </div>
              <div style={{flex: 1}}>
                <label style={{fontWeight: 700, color: '#fff'}}>Publish dir</label>
                <input value={netlifyPublishDir} onChange={e => setNetlifyPublishDir(e.target.value)} style={{width: '100%', background: '#23234b', color: '#fff', border: '1.5px solid #333', borderRadius: 10, padding: 10, fontSize: 15, marginTop: 8}} />
              </div>
            </div>
          )}
        </div>

        <button onClick={runPipeline} disabled={loading} style={{width: '100%', background: loading ? '#23234b' : 'linear-gradient(90deg,#6c63ff 0%,#48c6ef 100%)', color: loading ? '#aaa' : '#fff', border: 'none', borderRadius: 10, fontWeight: 800, fontSize: 18, padding: '14px 0', marginTop: 10, boxShadow: loading ? 'none' : '0 2px 12px #6c63ff33', cursor: loading ? 'not-allowed' : 'pointer', transition: 'all 0.2s', letterSpacing: 0.5}}>
          {loading ? 'Running...' : 'Run Pipeline'}
        </button>

        {error && <pre style={{color: '#ff4d4f', background: '#1a1a1a', borderRadius: 10, padding: 14, marginTop: 22, fontSize: 16, whiteSpace: 'pre-wrap', fontWeight: 600}}>{error}</pre>}
        {result && (
          <div style={{marginTop: 32, background: 'linear-gradient(135deg,#23234b 60%,#23234b 100%)', borderRadius: 14, padding: 22, color: '#fff', boxShadow: '0 2px 16px #0004', maxHeight: 420, overflowY: 'auto'}}>
            <h3 style={{margin: 0, fontWeight: 800, fontSize: 20, color: '#6c63ff', letterSpacing: 0.5, marginBottom: 12}}>Pipeline Plan</h3>
            <div style={{fontSize: 16, lineHeight: 1.7, color: '#e6e6fa'}}>
              <ReactMarkdown>{result.plan || result.result || JSON.stringify(result, null, 2)}</ReactMarkdown>
            </div>
          </div>
        )}

        <hr style={{margin: '38px 0 22px 0', border: 'none', borderTop: '1.5px solid #23234b'}}/>
        <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
          <a href="/github/login/" style={{color: '#fff', textDecoration: 'none', fontWeight: 700, fontSize: 16, display: 'flex', alignItems: 'center', gap: 8, letterSpacing: 0.2}}>
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" style={{verticalAlign: 'middle'}}><path d="M12 2C6.48 2 2 6.58 2 12.26c0 4.49 2.87 8.3 6.84 9.64.5.09.68-.22.68-.48 0-.24-.01-.87-.01-1.7-2.78.62-3.37-1.36-3.37-1.36-.45-1.18-1.1-1.5-1.1-1.5-.9-.63.07-.62.07-.62 1 .07 1.53 1.05 1.53 1.05.89 1.56 2.34 1.11 2.91.85.09-.66.35-1.11.63-1.37-2.22-.26-4.56-1.14-4.56-5.07 0-1.12.39-2.03 1.03-2.75-.1-.26-.45-1.3.1-2.7 0 0 .84-.28 2.75 1.05A9.38 9.38 0 0 1 12 7.07c.85.004 1.71.12 2.51.35 1.91-1.33 2.75-1.05 2.75-1.05.55 1.4.2 2.44.1 2.7.64.72 1.03 1.63 1.03 2.75 0 3.94-2.34 4.81-4.57 5.07.36.32.68.94.68 1.9 0 1.37-.01 2.47-.01 2.81 0 .27.18.58.69.48A10.01 10.01 0 0 0 22 12.26C22 6.58 17.52 2 12 2Z" fill="#fff"/></svg>
            Login with GitHub
          </a>
          <a href="/github/callback/" style={{color: '#b3b3e6', fontSize: 15, textDecoration: 'underline', fontWeight: 500}}>Callback (handled by backend)</a>
        </div>
      </div>
    </div>
  )
}

export default App
