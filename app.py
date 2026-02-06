import streamlit as st
import streamlit.components.v1 as components

# 1. Konfigurasi Streamlit (Wide Mode)
st.set_page_config(
    page_title="TikTok Downloader Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. CSS untuk Full Screen & No Padding
st.markdown("""
    <style>
        .block-container { padding: 0rem; }
        header { visibility: hidden; }
        footer { visibility: hidden; }
        iframe { width: 100%; border: none; }
        #MainMenu { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# 3. Kode HTML, CSS, JS
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
            background: linear-gradient(135deg, #000000 0%, #121212 100%);
            min-height: 100vh;
            color: white;
            margin: 0;
            padding: 40px 20px;
        }
        .glass {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .tiktok-gradient {
            background: linear-gradient(90deg, #ff0050 0%, #00f2ea 100%);
        }
        .loader {
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-top: 2px solid #ff0050;
            border-radius: 50%;
            width: 18px;
            height: 18px;
            animation: spin 0.8s linear infinite;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .custom-scrollbar::-webkit-scrollbar { width: 5px; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.2); border-radius: 10px; }
    </style>
</head>
<body>

    <div class="max-w-4xl mx-auto">
        <header class="text-center mb-10">
            <h1 class="text-4xl font-black mb-2 tracking-tighter italic">TIKTOK <span class="text-[#00f2ea]">PRO</span></h1>
            <p class="text-gray-500 text-sm">Download Video, Audio, dan Slideshow Foto</p>
        </header>

        <div class="glass p-5 rounded-2xl mb-8">
            <div class="flex flex-col md:flex-row gap-3">
                <input type="text" id="tiktokUrl" placeholder="Tempel link TikTok di sini..." 
                       class="flex-1 bg-white/5 border border-white/10 rounded-xl py-4 px-5 focus:outline-none focus:ring-1 focus:ring-[#00f2ea] transition-all">
                <button onclick="handleFetch()" id="fetchBtn" class="tiktok-gradient px-10 py-4 rounded-xl font-bold text-black flex items-center justify-center gap-2">
                    <span id="btnText">AMBIL</span>
                    <div id="btnLoader" class="loader hidden"></div>
                </button>
            </div>
        </div>

        <div id="resultArea" class="hidden space-y-6">
            <div class="glass rounded-3xl overflow-hidden md:flex">
                <div class="md:w-1/3 bg-black">
                    <img id="videoThumb" src="" class="w-full h-full object-contain aspect-[9/16]">
                </div>
                <div class="md:w-2/3 p-8 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center gap-3 mb-5">
                            <img id="authorImg" src="" class="w-12 h-12 rounded-full border border-white/10">
                            <div>
                                <h3 id="authorName" class="font-bold">Username</h3>
                                <p id="authorId" class="text-gray-500 text-sm">@id</p>
                            </div>
                        </div>
                        <p id="videoDesc" class="text-gray-300 mb-6 text-sm line-clamp-3 italic"></p>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <button id="dlVideo" class="bg-white text-black font-bold py-4 rounded-xl flex items-center justify-center gap-2 hover:bg-gray-200">
                            <i data-lucide="video"></i> Video (.mp4)
                        </button>
                        <button id="dlAudio" class="bg-white/10 text-white font-bold py-4 rounded-xl flex items-center justify-center gap-2 hover:bg-white/20 border border-white/10">
                            <i data-lucide="music"></i> Audio (.mp3)
                        </button>
                    </div>
                </div>
            </div>

            <div id="photosSection" class="hidden">
                <h3 class="text-xl font-bold mb-4 flex items-center gap-2">
                    <i data-lucide="image" class="text-[#00f2ea]"></i> Galeri Foto
                </h3>
                <div id="photosGrid" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">
                    </div>
            </div>
        </div>
        
        <footer class="mt-10 text-center text-gray-600 text-[10px] tracking-widest uppercase">
            &copy; 2026 Developed by @vixelboy
        </footer>
    </div>

    <script>
        lucide.createIcons();

        // FUNGSI UTAMA DOWNLOAD (Direct Download via Blob)
        async function directDownload(url, filename, btnId) {
            const btn = document.getElementById(btnId);
            const originalHtml = btn.innerHTML;
            btn.innerHTML = '<div class="loader"></div>';
            btn.disabled = true;

            try {
                const response = await fetch(url);
                const blob = await response.blob();
                const blobUrl = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = blobUrl;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(blobUrl);
            } catch (err) {
                console.error("Gagal download:", err);
                window.open(url, '_blank'); // Fallback jika gagal
            } finally {
                btn.innerHTML = originalHtml;
                btn.disabled = false;
            }
        }

        async function handleFetch() {
            const url = document.getElementById('tiktokUrl').value.trim();
            if(!url) return;

            document.getElementById('btnText').classList.add('hidden');
            document.getElementById('btnLoader').classList.remove('hidden');

            try {
                const res = await fetch(`https://www.tikwm.com/api/?url=${encodeURIComponent(url)}`);
                const json = await res.json();
                
                if(json.code === 0) {
                    const data = json.data;
                    document.getElementById('videoThumb').src = data.cover;
                    document.getElementById('authorImg').src = data.author.avatar;
                    document.getElementById('authorName').textContent = data.author.nickname;
                    document.getElementById('authorId').textContent = `@${data.author.unique_id}`;
                    document.getElementById('videoDesc').textContent = data.title || "";

                    // Setup Download Buttons
                    document.getElementById('dlVideo').onclick = () => directDownload(data.play, `tiktok_video_${data.id}.mp4`, 'dlVideo');
                    document.getElementById('dlAudio').onclick = () => directDownload(data.music, `tiktok_audio_${data.id}.mp3`, 'dlAudio');

                    // Setup Photos if available
                    const photoSection = document.getElementById('photosSection');
                    const photoGrid = document.getElementById('photosGrid');
                    photoGrid.innerHTML = '';
                    
                    if(data.images && data.images.length > 0) {
                        photoSection.classList.remove('hidden');
                        data.images.forEach((img, i) => {
                            const div = document.createElement('div');
                            div.className = "relative group rounded-xl overflow-hidden aspect-[9/16] glass";
                            div.innerHTML = `
                                <img src="${img}" class="w-full h-full object-cover">
                                <button onclick="directDownload('${img}', 'foto_${i+1}.jpg', this.id)" id="img_${i}" 
                                        class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                                    <i data-lucide="download" class="text-white"></i>
                                </button>
                            `;
                            photoGrid.appendChild(div);
                        });
                        lucide.createIcons();
                    } else {
                        photoSection.classList.add('hidden');
                    }

                    document.getElementById('resultArea').classList.remove('hidden');
                }
            } catch (e) { alert("Terjadi kesalahan koneksi."); }
            finally {
                document.getElementById('btnText').classList.remove('hidden');
                document.getElementById('btnLoader').classList.add('hidden');
            }
        }
    </script>
</body>
</html>
"""

# Menampilkan ke Streamlit dengan tinggi yang menyesuaikan
components.html(html_code, height=1200, scrolling=True)
