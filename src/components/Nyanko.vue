<script setup>
import { ref, computed, onMounted } from 'vue'

const search = ref('')
const selectedChapter = ref('전체')
const chapters = ref([])
const loading = ref(true)
const youtubeData = ref({})
const youtubeLoading = ref({})

onMounted(async () => {
  const res = await fetch('http://localhost:8000/chapters')
  chapters.value = await res.json()
  loading.value = false
})

const chapterNames = computed(() => ['전체', ...chapters.value.map(c => c.name)])

const filtered = computed(() => {
  const q = search.value
  const list = chapters.value
  if (selectedChapter.value === '전체') {
    return list.map(chapter => ({
      ...chapter,
      stages: chapter.stages.filter(s =>
        s.name.includes(q) || s.enemies.some(e => e.includes(q)) || s.strategy.includes(q)
      )
    })).filter(c => c.stages.length > 0)
  }
  return list
    .filter(c => c.name === selectedChapter.value)
    .map(chapter => ({
      ...chapter,
      stages: chapter.stages.filter(s =>
        s.name.includes(q) || s.enemies.some(e => e.includes(q)) || s.strategy.includes(q)
      )
    }))
})

async function fetchYoutube(stageName) {
  if (youtubeData.value[stageName]) return
  youtubeLoading.value[stageName] = true
  try {
    const res = await fetch(`http://localhost:8000/youtube?stage=${encodeURIComponent(stageName)}`)
    youtubeData.value[stageName] = await res.json()
  } catch {
    youtubeData.value[stageName] = { error: '검색 실패' }
  } finally {
    youtubeLoading.value[stageName] = false
  }
}

function formatViews(n) {
  if (!n) return ''
  if (n >= 10000) return `${Math.floor(n / 10000)}만회`
  if (n >= 1000) return `${Math.floor(n / 1000)}천회`
  return `${n}회`
}
</script>

<template>
  <div>
    <div class="page-header">
      <h1>🐱 냥코대전쟁</h1>
      <p class="subtitle">레전드 스토리 스테이지별 적 캐릭터 & 공략법</p>
    </div>

    <div class="controls">
      <input v-model="search" placeholder="스테이지명, 캐릭터, 공략 키워드 검색..." class="search" />
      <select v-model="selectedChapter" class="chapter-select">
        <option v-for="name in chapterNames" :key="name" :value="name">{{ name }}</option>
      </select>
    </div>

    <div v-if="loading" class="empty">데이터 불러오는 중... 🐱</div>

    <div v-for="chapter in filtered" :key="chapter.name" class="chapter">
      <h2 class="chapter-title">📖 {{ chapter.name }}</h2>
      <div class="chapter-tip">💡 {{ chapter.tip }}</div>
      <div class="stage-list">
        <div v-for="stage in chapter.stages" :key="stage.name" class="stage-card">
          <div class="stage-name">⚔️ {{ stage.name }}</div>
          <div class="enemies">
            <span v-if="stage.enemies.length === 0" class="no-enemy">적 없음</span>
            <span v-for="e in stage.enemies" :key="e" class="enemy-tag">{{ e }}</span>
          </div>
          <div class="strategy">🗺 {{ stage.strategy }}</div>
          <div class="youtube-section">
            <button
              v-if="!youtubeData[stage.name]"
              class="yt-btn"
              :disabled="youtubeLoading[stage.name]"
              @click="fetchYoutube(stage.name)"
            >
              {{ youtubeLoading[stage.name] ? '검색 중...' : '▶ 공략 영상 보기' }}
            </button>
            <div v-if="youtubeData[stage.name] && !youtubeData[stage.name].error" class="yt-result">
              <a :href="youtubeData[stage.name].url" target="_blank" class="yt-link">
                <img :src="youtubeData[stage.name].thumbnail" class="yt-thumb" />
                <div class="yt-info">
                  <div class="yt-title">{{ youtubeData[stage.name].title }}</div>
                  <div class="yt-meta">
                    {{ youtubeData[stage.name].channel }} · 조회수 {{ formatViews(youtubeData[stage.name].view_count) }}
                  </div>
                </div>
              </a>
            </div>
            <div v-if="youtubeData[stage.name]?.error" class="yt-error">영상을 찾을 수 없어요</div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!loading && filtered.length === 0" class="empty">검색 결과가 없어요 😿</div>
  </div>
</template>

<style scoped>
.page-header { text-align: center; margin-bottom: 1.5rem; }
.page-header h1 { font-size: 2.2rem; margin-bottom: 0.3rem; }
.subtitle { color: #666; }

.controls { display: flex; flex-direction: column; gap: 0.8rem; align-items: center; margin-bottom: 2rem; }

.search, .chapter-select {
  width: 100%;
  max-width: 560px;
  padding: 0.7rem 1rem;
  font-size: 1rem;
  border: 2px solid #ddd;
  border-radius: 10px;
  outline: none;
  background: white;
}
.search:focus, .chapter-select:focus { border-color: #42b883; }

.chapter { margin-bottom: 2.5rem; }

.chapter-title {
  font-size: 1.2rem;
  font-weight: bold;
  color: #2d8a5e;
  border-left: 4px solid #42b883;
  padding-left: 0.7rem;
  margin-bottom: 0.5rem;
}

.chapter-tip {
  background: #f0faf5;
  border: 1px solid #b2dfcb;
  border-radius: 8px;
  padding: 0.6rem 1rem;
  font-size: 0.88rem;
  color: #2d6a4f;
  margin-bottom: 0.8rem;
}

.stage-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 0.7rem;
}

.stage-card {
  background: #fafafa;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 0.9rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  transition: box-shadow 0.15s;
}
.stage-card:hover { box-shadow: 0 2px 10px rgba(0,0,0,0.1); }

.stage-name { font-weight: bold; font-size: 0.95rem; color: #333; }

.enemies { display: flex; flex-wrap: wrap; gap: 0.3rem; }

.enemy-tag {
  background: #e8f5ef;
  color: #2d8a5e;
  border: 1px solid #b2dfcb;
  border-radius: 12px;
  padding: 0.15rem 0.55rem;
  font-size: 0.76rem;
}

.no-enemy { color: #bbb; font-size: 0.8rem; }

.strategy {
  font-size: 0.82rem;
  color: #555;
  line-height: 1.5;
  border-top: 1px solid #eee;
  padding-top: 0.4rem;
}

.empty { text-align: center; margin-top: 3rem; font-size: 1.2rem; color: #aaa; }

.youtube-section { margin-top: 0.6rem; border-top: 1px solid #eee; padding-top: 0.5rem; }

.yt-btn {
  width: 100%;
  padding: 0.45rem;
  background: #ff0000;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.82rem;
  font-weight: bold;
  transition: background 0.2s;
}
.yt-btn:hover { background: #cc0000; }
.yt-btn:disabled { background: #aaa; cursor: default; }

.yt-result { margin-top: 0.4rem; }

.yt-link {
  display: flex;
  gap: 0.6rem;
  align-items: flex-start;
  text-decoration: none;
  color: inherit;
}
.yt-link:hover .yt-title { text-decoration: underline; }

.yt-thumb {
  width: 100px;
  height: 56px;
  object-fit: cover;
  border-radius: 6px;
  flex-shrink: 0;
}

.yt-info { flex: 1; }

.yt-title {
  font-size: 0.78rem;
  font-weight: bold;
  color: #222;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.yt-meta { font-size: 0.72rem; color: #888; margin-top: 0.2rem; }
.yt-error { font-size: 0.78rem; color: #aaa; margin-top: 0.3rem; }
</style>
