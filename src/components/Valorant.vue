<script setup>
import { ref, computed, onMounted } from 'vue'
import BASE_URL from '../api.js'

const agents = ref([])
const search = ref('')
const selectedRole = ref('전체')

const roles = ['전체', '타격대', '척후대', '전략가', '감시자']
const roleEmoji = { '타격대': '⚔️', '척후대': '🔍', '전략가': '🌫️', '감시자': '🛡️' }
const roleColor = { '타격대': '#e74c3c', '척후대': '#f39c12', '전략가': '#8e44ad', '감시자': '#27ae60' }
const difficultyColor = { '쉬움': '#27ae60', '보통': '#f39c12', '어려움': '#e74c3c' }

onMounted(async () => {
  const res = await fetch(`${BASE_URL}/agents`)
  agents.value = await res.json()
})

const filtered = computed(() => {
  return agents.value.filter(a => {
    const matchRole = selectedRole.value === '전체' || a.role === selectedRole.value
    const matchSearch = a.name.includes(search.value) || a.description.includes(search.value)
    return matchRole && matchSearch
  })
})

const selectedAgent = ref(null)
function selectAgent(agent) {
  selectedAgent.value = selectedAgent.value?.name === agent.name ? null : agent
}
</script>

<template>
  <div class="valorant-wrap">
    <div class="valo-header">
      <h1>🎯 발로란트</h1>
      <p class="subtitle">요원 특징 & 스킬 가이드</p>
    </div>

    <div class="controls">
      <input v-model="search" placeholder="요원 이름 또는 특징 검색..." class="search" />
      <div class="role-buttons">
        <button
          v-for="role in roles"
          :key="role"
          :class="['role-btn', { active: selectedRole === role }]"
          :style="selectedRole === role && role !== '전체' ? { background: roleColor[role], borderColor: roleColor[role] } : {}"
          @click="selectedRole = role"
        >
          {{ roleEmoji[role] ?? '📋' }} {{ role }}
        </button>
      </div>
    </div>

    <p class="count">{{ filtered.length }}명의 요원</p>

    <div class="agent-grid">
      <div
        v-for="agent in filtered"
        :key="agent.name"
        :class="['agent-card', { selected: selectedAgent?.name === agent.name }]"
        :style="{ borderColor: roleColor[agent.role] }"
        @click="selectAgent(agent)"
      >
        <div class="agent-top">
          <div>
            <div class="agent-name">{{ agent.name }}</div>
            <div class="agent-origin">📍 {{ agent.origin }}</div>
          </div>
          <div class="badges">
            <span class="role-badge" :style="{ background: roleColor[agent.role] }">
              {{ roleEmoji[agent.role] }} {{ agent.role }}
            </span>
            <span class="diff-badge" :style="{ color: difficultyColor[agent.difficulty] }">
              {{ agent.difficulty }}
            </span>
          </div>
        </div>

        <p class="agent-desc">{{ agent.description }}</p>

        <!-- 펼쳐지는 스킬 정보 -->
        <div v-if="selectedAgent?.name === agent.name" class="agent-detail">
          <div class="skills">
            <div v-for="skill in agent.skills" :key="skill.name" class="skill-item">
              <span class="skill-type" :class="skill.type">{{ skill.type }}</span>
              <span class="skill-name">{{ skill.name }}</span>
              <span class="skill-desc">{{ skill.desc }}</span>
            </div>
          </div>
          <div class="agent-tip">💡 {{ agent.tip }}</div>
        </div>

        <div class="expand-hint">{{ selectedAgent?.name === agent.name ? '▲ 접기' : '▼ 스킬 보기' }}</div>
      </div>
    </div>

    <div v-if="filtered.length === 0" class="empty">검색 결과가 없어요 😢</div>
  </div>
</template>

<style scoped>
.valorant-wrap { padding: 0; }

.valo-header { text-align: center; margin-bottom: 1.5rem; }
.valo-header h1 { font-size: 2.2rem; margin-bottom: 0.3rem; }
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
.search:focus { border-color: #ff4655; }

.role-buttons { display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center; }

.role-btn {
  padding: 0.4rem 0.9rem;
  border: 2px solid #ddd;
  border-radius: 20px;
  background: white;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
  font-weight: bold;
}
.role-btn.active { color: white; }

.count { text-align: center; color: #888; font-size: 0.9rem; margin-bottom: 1.2rem; }

.agent-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.agent-card {
  border: 2px solid #ddd;
  border-radius: 12px;
  padding: 1rem;
  cursor: pointer;
  transition: box-shadow 0.2s, transform 0.15s;
  background: white;
}
.agent-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.12); transform: translateY(-2px); }
.agent-card.selected { background: #fafafa; }

.agent-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem; }

.agent-name { font-size: 1.1rem; font-weight: bold; color: #222; }
.agent-origin { font-size: 0.78rem; color: #888; margin-top: 0.1rem; }

.badges { display: flex; flex-direction: column; align-items: flex-end; gap: 0.3rem; }

.role-badge {
  color: white;
  font-size: 0.72rem;
  font-weight: bold;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
}

.diff-badge { font-size: 0.72rem; font-weight: bold; }

.agent-desc { font-size: 0.83rem; color: #555; line-height: 1.5; margin-bottom: 0.5rem; }

.agent-detail { margin-top: 0.8rem; border-top: 1px solid #eee; padding-top: 0.8rem; }

.skills { display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 0.8rem; }

.skill-item { display: flex; align-items: flex-start; gap: 0.5rem; font-size: 0.8rem; }

.skill-type {
  font-size: 0.68rem;
  font-weight: bold;
  padding: 0.15rem 0.4rem;
  border-radius: 6px;
  white-space: nowrap;
  flex-shrink: 0;
}
.skill-type.기본 { background: #e8f5ef; color: #2d8a5e; }
.skill-type.고유 { background: #fff3e0; color: #e65c00; }
.skill-type.궁극기 { background: #fce4ec; color: #c62828; }

.skill-name { font-weight: bold; color: #333; white-space: nowrap; }
.skill-desc { color: #666; }

.agent-tip {
  background: #fff8e1;
  border-left: 3px solid #ffc107;
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
  .role-buttons { gap: 0.3rem; }
  .role-btn { font-size: 0.78rem; padding: 0.3rem 0.6rem; }
  .agent-grid { grid-template-columns: 1fr; }
  .agent-card { padding: 0.85rem; }
}
</style>
