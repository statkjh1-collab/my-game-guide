<script setup>
import { ref, computed, onMounted } from 'vue'
import BASE_URL from '../api.js'

const mobs = ref([])
const search = ref('')
const selectedType = ref('전체')
const selectedMob = ref(null)

const types = ['전체', '평화적', '중립적', '적대적', '보스']
const typeEmoji = { '평화적': '🐾', '중립적': '😐', '적대적': '⚔️', '보스': '💀' }
const typeColor = { '평화적': '#27ae60', '중립적': '#f39c12', '적대적': '#e74c3c', '보스': '#8e44ad' }

onMounted(async () => {
  const res = await fetch(`${BASE_URL}/mobs`)
  mobs.value = await res.json()
})

const filtered = computed(() => {
  return mobs.value.filter(m => {
    const matchType = selectedType.value === '전체' || m.type === selectedType.value
    const matchSearch = m.name.includes(search.value) || m.description.includes(search.value) || m.biome.includes(search.value)
    return matchType && matchSearch
  })
})

function toggleMob(mob) {
  selectedMob.value = selectedMob.value?.name === mob.name ? null : mob
}
</script>

<template>
  <div>
    <div class="page-header">
      <h1>⛏️ 마인크래프트</h1>
      <p class="subtitle">몹 도감 & 공략 가이드</p>
    </div>

    <div class="controls">
      <input v-model="search" placeholder="몹 이름, 특징, 바이옴 검색..." class="search" />
      <div class="type-buttons">
        <button
          v-for="type in types"
          :key="type"
          :class="['type-btn', { active: selectedType === type }]"
          :style="selectedType === type && type !== '전체' ? { background: typeColor[type], borderColor: typeColor[type] } : {}"
          @click="selectedType = type"
        >
          {{ typeEmoji[type] ?? '📋' }} {{ type }}
        </button>
      </div>
    </div>

    <p class="count">{{ filtered.length }}종의 몹</p>

    <div class="mob-grid">
      <div
        v-for="mob in filtered"
        :key="mob.name"
        :class="['mob-card', { selected: selectedMob?.name === mob.name }]"
        :style="{ borderColor: typeColor[mob.type] }"
        @click="toggleMob(mob)"
      >
        <div class="mob-top">
          <div>
            <div class="mob-name">{{ mob.name }}</div>
            <div class="mob-biome">🌍 {{ mob.biome }}</div>
          </div>
          <div class="mob-badges">
            <span class="type-badge" :style="{ background: typeColor[mob.type] }">
              {{ typeEmoji[mob.type] }} {{ mob.type }}
            </span>
          </div>
        </div>

        <p class="mob-desc">{{ mob.description }}</p>

        <div class="mob-stats">
          <span class="stat hp">❤️ {{ mob.hp }}</span>
          <span class="stat atk" v-if="mob.attack > 0">⚔️ {{ mob.attack }}</span>
          <span class="stat atk" v-else>🕊️ 무해</span>
        </div>

        <!-- 펼쳐지는 상세 정보 -->
        <div v-if="selectedMob?.name === mob.name" class="mob-detail">
          <div v-if="mob.drops.length > 0" class="drops">
            <span class="detail-label">📦 드롭</span>
            <span v-for="d in mob.drops" :key="d" class="drop-tag">{{ d }}</span>
          </div>
          <div class="mob-tip">💡 {{ mob.tip }}</div>
        </div>

        <div class="expand-hint">{{ selectedMob?.name === mob.name ? '▲ 접기' : '▼ 상세 보기' }}</div>
      </div>
    </div>

    <div v-if="filtered.length === 0" class="empty">검색 결과가 없어요 🪨</div>
  </div>
</template>

<style scoped>
.page-header { text-align: center; margin-bottom: 1.5rem; }
.page-header h1 { font-size: 2.2rem; margin-bottom: 0.3rem; }
.subtitle { color: #666; }

.controls { display: flex; flex-direction: column; gap: 0.8rem; align-items: center; margin-bottom: 1rem; }

.search {
  width: 100%;
  max-width: 500px;
  padding: 0.7rem 1rem;
  font-size: 1rem;
  border: 2px solid #ddd;
  border-radius: 10px;
  outline: none;
}
.search:focus { border-color: #5d8a3c; }

.type-buttons { display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center; }

.type-btn {
  padding: 0.4rem 0.9rem;
  border: 2px solid #ddd;
  border-radius: 20px;
  background: white;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: bold;
  transition: all 0.2s;
}
.type-btn.active { color: white; }

.count { text-align: center; color: #888; font-size: 0.9rem; margin-bottom: 1.2rem; }

.mob-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.mob-card {
  border: 2px solid #ddd;
  border-radius: 12px;
  padding: 1rem;
  cursor: pointer;
  background: white;
  transition: box-shadow 0.2s, transform 0.15s;
}
.mob-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.12); transform: translateY(-2px); }
.mob-card.selected { background: #fafafa; }

.mob-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem; }

.mob-name { font-size: 1.05rem; font-weight: bold; color: #222; }
.mob-biome { font-size: 0.75rem; color: #888; margin-top: 0.2rem; }

.type-badge {
  color: white;
  font-size: 0.72rem;
  font-weight: bold;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  white-space: nowrap;
}

.mob-desc { font-size: 0.83rem; color: #555; line-height: 1.5; margin-bottom: 0.5rem; }

.mob-stats { display: flex; gap: 0.8rem; margin-bottom: 0.3rem; }
.stat { font-size: 0.82rem; font-weight: bold; }
.hp { color: #e74c3c; }
.atk { color: #e67e22; }

.mob-detail { margin-top: 0.8rem; border-top: 1px solid #eee; padding-top: 0.8rem; display: flex; flex-direction: column; gap: 0.6rem; }

.drops { display: flex; flex-wrap: wrap; gap: 0.4rem; align-items: center; }
.detail-label { font-size: 0.78rem; font-weight: bold; color: #555; }

.drop-tag {
  background: #fff3cd;
  border: 1px solid #ffc107;
  color: #856404;
  border-radius: 10px;
  padding: 0.15rem 0.5rem;
  font-size: 0.75rem;
}

.mob-tip {
  background: #f0f7ff;
  border-left: 3px solid #3498db;
  padding: 0.5rem 0.7rem;
  font-size: 0.8rem;
  color: #555;
  border-radius: 0 6px 6px 0;
}

.expand-hint { text-align: center; font-size: 0.75rem; color: #aaa; margin-top: 0.6rem; }

.empty { text-align: center; margin-top: 3rem; font-size: 1.2rem; color: #aaa; }

@media (max-width: 768px) {
  .page-header h1 { font-size: 1.6rem; }
  .search { font-size: 0.95rem; }
  .type-btn { font-size: 0.8rem; padding: 0.35rem 0.7rem; }
  .mob-grid { grid-template-columns: 1fr; }
  .mob-card { padding: 0.85rem; }
}
</style>
