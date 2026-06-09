<script setup>
import { ref } from 'vue'
import Nyanko from './components/Nyanko.vue'
import Valorant from './components/Valorant.vue'
import Minecraft from './components/Minecraft.vue'

const currentPage = ref('nyanko')

const menus = [
  { key: 'nyanko',    label: '냥코대전쟁', icon: '🐱' },
  { key: 'valorant',  label: '발로란트',   icon: '🎯' },
  { key: 'minecraft', label: '마인크래프트', icon: '⛏️' },
]
</script>

<template>
  <div class="app-layout">
    <!-- 사이드바 -->
    <aside class="sidebar">
      <div class="sidebar-logo">🎮 게임 가이드</div>
      <nav class="sidebar-nav">
        <button
          v-for="menu in menus"
          :key="menu.key"
          :class="['nav-item', { active: currentPage === menu.key }]"
          @click="currentPage = menu.key"
        >
          <span class="nav-icon">{{ menu.icon }}</span>
          <span class="nav-label">{{ menu.label }}</span>
        </button>
      </nav>
    </aside>

    <!-- 메인 콘텐츠 -->
    <main class="main-content">
      <Nyanko v-if="currentPage === 'nyanko'" />
      <Valorant v-if="currentPage === 'valorant'" />
      <Minecraft v-if="currentPage === 'minecraft'" />
    </main>
  </div>
</template>

<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Arial', sans-serif; background: #f4f6f8; }
</style>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
}

/* 사이드바 */
.sidebar {
  width: 200px;
  min-height: 100vh;
  background: #1a1a2e;
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
}

.sidebar-logo {
  padding: 1.5rem 1.2rem;
  font-size: 1.1rem;
  font-weight: bold;
  color: white;
  border-bottom: 1px solid #2d2d4e;
  letter-spacing: 0.5px;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  padding: 1rem 0.7rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 10px;
  background: transparent;
  color: #aaa;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: bold;
  transition: all 0.2s;
  text-align: left;
  width: 100%;
}
.nav-item:hover { background: #2d2d4e; color: white; }
.nav-item.active { background: #4f46e5; color: white; }

.nav-icon { font-size: 1.2rem; }

/* 메인 콘텐츠 */
.main-content {
  margin-left: 200px;
  flex: 1;
  padding: 2rem 2.5rem;
  max-width: calc(100vw - 200px);
}
</style>
