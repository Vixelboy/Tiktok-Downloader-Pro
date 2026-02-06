import streamlit as st
import streamlit.components.v1 as components

# 1. Setting agar layout Streamlit lebar (Wide Mode)
st.set_page_config(
    page_title="TikTok Downloader Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. CSS tambahan untuk menghilangkan padding bawaan Streamlit agar HTML benar-benar Full
st.markdown("""
    <style>
        /* Menghilangkan padding utama Streamlit */
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
        }
        /* Menghilangkan header default Streamlit */
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Memastikan iframe komponen HTML mengisi layar */
        iframe {
            width: 100%;
            border: none;
        }
    </style>
    """, unsafe_allow_html=True)

# 3. Masukkan kode HTML kamu
html_code = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
            min-height: 100vh;
            color: white;
            margin: 0;
            padding: 40px 20px;
        }

        .glass {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .tiktok-gradient {
            background: linear-gradient(90deg, #ff0050 0%, #00f2ea 100%);
        }

        .loader {
            border: 3px solid rgba(255, 255, 255, 0.1);
            border-top: 3px solid #ff0050;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .custom-scrollbar::-webkit-scrollbar { width: 6px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: rgba(255, 255, 255, 0.05); }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.2); border-radius: 10px; }
    </style>
</head>
<body>

    <div class="max-w-4xl mx-auto">
        <header class="text-center mb-12">
            <div class="inline-flex items-center justify-center p-3 mb-4 rounded-2xl glass border border-white/10">
                <i data-lucide="download-cloud" class="w-8 h-8 text-[#ff0050]"></i>
            </div>
            <h1 class="text-4xl font-extrabold mb-2 tracking-tight">TikTok <span class="text-[#00f2ea]">Downloader</span></h1>
            <p class="text-gray-400">Unduh video (tanpa watermark) & foto slideshow TikTok dengan mudah.</p>
        </header>

        <div class="glass p-6 rounded-3xl shadow-2xl border border-white/10 mb-8">
            <div class="flex flex-col md:flex-row gap-4">
                <div class="relative flex-1">
                    <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                        <i data-lucide="link" class="w-5 h-5 text-gray-500"></i>
                    </div>
                    <input 
                        type="text" 
                        id="tiktokUrl"
                        placeholder="Tempel tautan video atau foto TikTok di sini..." 
                        class="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 focus:outline-none focus:ring-2 focus:ring-[#ff0050]/50 transition-all text-white placeholder-gray-500"
                    >
                </div>
                <button onclick="handleFetch()" id="fetchBtn" class="tiktok-gradient px-8 py-4 rounded-2xl font-bold text-black hover:opacity-90 transition-all flex items-center justify-center gap-2 min-w-[160px]">
                    <span id="btnText">Ambil Data</span>
                    <div id="btnLoader" class="loader hidden"></div>
                </button>
            </div>
            <p id="errorMessage" class="text-red-400 text-sm mt-4 hidden items-center gap-2">
                <i data-lucide="alert-circle" class="w-4 h-4"></i>
                <span id="errorText">Tautan tidak valid.</span>
            </p>
        </div>

        <div id="resultArea" class="hidden space-y-6">
            <div class="glass rounded-3xl overflow-hidden border border-white/10">
                <div class="md:flex">
                    <div class="md:w-1/3 relative group bg-black flex items-center justify-center">
                        <img id="videoThumb" src="" alt="Thumbnail" class="w-full h-full object-contain aspect-[9/16]">
                    </div>
                    <div class="md:w-2/3 p-6 flex flex-col justify-between">
                        <div>
                            <div class="flex items-center gap-3 mb-4">
                                <img id="authorImg" src="" class="w-12 h-12 rounded-full border border-white/20">
                                <div>
                                    <h3 id="authorName" class="font-bold text-lg leading-tight">Username</h3>
                                    <p id="authorUsername" class="text-gray-400 text-sm">@nickname</p>
                                </div>
                            </div>
                            <p id="videoDesc" class="text-gray-300 text-sm mb-6 italic">Judul konten...</p>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                            <button id="hdBtn" class="flex items-center justify-center gap-2 bg-white text-black font-bold py-4 rounded-xl hover:bg-gray-200 transition-colors">
                                <i data-lucide="video" class="w-5 h-5"></i>
                                <span>Unduh Video</span>
                            </button>
                            <button id="musicBtn" class="flex items-center justify-center gap-2 bg-white/10 text-white font-bold py-4 rounded-xl hover:bg-white/20 transition-colors border border-white/10">
                                <i data-lucide="music" class="w-5 h-5"></i>
                                <span>Unduh Audio</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <footer class="mt-12 text-center text-gray-500 text-sm">
            <p>&copy; 2026 TikTok Downloader Pro. by : @vixelboy</p>
        </footer>
    </div>

    <script>
        lucide.createIcons();
        async function handleFetch() {
            const urlInput = document.getElementById('tiktokUrl');
            const url = urlInput.value.trim();
            if (!url) return;

            document.getElementById('btnText').textContent = "Memproses...";
            document.getElementById('btnLoader').classList.remove('hidden');
            
            try {
                const response = await fetch(`https://www.tikwm.com/api/?url=${encodeURIComponent(url)}`);
                const result = await response.json();
                if (result.code === 0) {
                    const data = result.data;
                    document.getElementById('videoThumb').src = data.cover;
                    document.getElementById('authorImg').src = data.author.avatar;
                    document.getElementById('authorName').textContent = data.author.nickname;
                    document.getElementById('authorUsername').textContent = `@${data.author.unique_id}`;
                    document.getElementById('videoDesc').textContent = data.title || "";
                    
                    document.getElementById('hdBtn').onclick = () => window.open(data.play, '_blank');
                    document.getElementById('musicBtn').onclick = () => window.open(data.music, '_blank');
                    document.getElementById('resultArea').classList.remove('hidden');
                }
            } catch (e) { console.error(e); }
            finally {
                document.getElementById('btnText').textContent = "Ambil Data";
                document.getElementById('btnLoader').classList.add('hidden');
            }
        }
    </script>
</body>
</html>
"""

# Menampilkan dengan tinggi 100vh agar memenuhi layar (atau cukup tinggi sesuai konten)
components.html(html_code, height=1000, scrolling=True)
