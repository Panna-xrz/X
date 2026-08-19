<script setup lang="ts">
import { ref, computed, type Component } from 'vue'
import { useMessage } from 'naive-ui'

// Panna AI 助手右侧常驻可折叠侧边栏
// - 4 种模式：聊天 / RAG / Agent / Panna
// - 设计面板与交互骨架，后端能力待实现

type PannaMode = 'chat' | 'rag' | 'agent' | 'panna'

const message = useMessage()

const collapsed = ref(false)
const mode = ref<PannaMode>('chat')
const input = ref('')

// 模式内联 SVG 图标
const ChatIcon: Component = {
  template: `
    <svg viewBox="0 0 24 24" width="20" height="24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
      <path d="M4 5h16v10H8l-4 4z" />
      <path d="M8 9h8M8 12h5" />
    </svg>
  `
}
const RagIcon: Component = {
  template: `
    <svg viewBox="0 0 24 24" width="20" height="24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="11" cy="11" r="6" />
      <path d="M15.5 15.5L20 20" />
      <path d="M8.5 11h5" />
    </svg>
  `
}
const AgentIcon: Component = {
  template: `
    <svg viewBox="0 0 24 24" width="20" height="24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
      <rect x="5" y="8" width="14" height="10" rx="2" />
      <path d="M12 4v4M9 14h.01M15 14h.01M9 17h6" />
      <path d="M3 13h2M19 13h2" />
    </svg>
  `
}
const PannaIcon: Component = {
  template: `
    <svg viewBox="0 0 24 24" width="20" height="24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 3a4 4 0 0 1 4 4v1a4 4 0 0 1-8 0V7a4 4 0 0 1 4-4z" />
      <path d="M6 21v-2a6 6 0 0 1 12 0v2" />
      <path d="M12 12v3" />
    </svg>
  `
}
const CollapseIcon: Component = {
  template: `
    <svg viewBox="0 0 24 24" width="20" height="24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
      <path d="M9 6l6 6-6 6" />
    </svg>
  `
}

interface ModeItem {
  key: PannaMode
  label: string
  desc: string
  icon: Component
}

const modes: ModeItem[] = [
  { key: 'chat', label: '聊天', desc: '与 Panna 自由对话，探讨设计思路与方案。', icon: ChatIcon },
  { key: 'rag', label: 'RAG', desc: '基于项目知识库检索问答，引用规范与历史文档。', icon: RagIcon },
  { key: 'agent', label: 'Agent', desc: '自主调用工具完成多步任务，如生成、检索、汇总。', icon: AgentIcon },
  { key: 'panna', label: 'Panna', desc: '综合模式：主动感知项目上下文，提供情境化建议。', icon: PannaIcon }
]

const currentMode = computed(() => modes.find((m) => m.key === mode.value)!)

function send() {
  if (!input.value.trim()) return
  // 后端待实现
  message.info('Panna 后端待接入，当前为前端面板骨架')
  input.value = ''
}
</script>

<template>
  <aside class="panna-rail" :class="{ collapsed }">
    <!-- 展开态：完整面板 -->
    <div v-show="!collapsed" class="panna-panel">
      <!-- 头部 -->
      <header class="panna-header">
        <div class="brand">
          <PannaIcon class="brand-icon" />
          <div class="brand-text">
            <div class="brand-name">Panna</div>
            <div class="brand-sub">AI 助手</div>
          </div>
        </div>
        <button class="icon-btn" title="收起" @click="collapsed = true">
          <CollapseIcon />
        </button>
      </header>

      <!-- 模式切换 -->
      <div class="mode-switch">
        <button
          v-for="m in modes"
          :key="m.key"
          class="mode-btn"
          :class="{ active: mode === m.key }"
          :title="m.desc"
          @click="mode = m.key"
        >
          <component :is="m.icon" class="mode-icon" />
          <span class="mode-label">{{ m.label }}</span>
        </button>
      </div>

      <!-- 内容区 -->
      <div class="panna-body">
        <div class="mode-hint">{{ currentMode.desc }}</div>
        <div class="message-list">
          <!-- 占位：后端接入后替换为真实消息流 -->
          <div class="empty-hint">
            <PannaIcon class="empty-icon" />
            <div class="empty-text">Panna 已就绪</div>
            <div class="empty-sub">后端能力接入后将在此显示对话</div>
          </div>
        </div>
      </div>

      <!-- 输入区 -->
      <footer class="panna-footer">
        <textarea
          v-model="input"
          class="input-area"
          rows="2"
          placeholder="输入消息…（后端待实现）"
          @keydown.enter.prevent="send"
        />
        <button class="send-btn" @click="send">发送</button>
      </footer>
    </div>

    <!-- 折叠态：窄条 -->
    <button
      v-show="collapsed"
      class="panna-collapsed"
      title="展开 Panna"
      @click="collapsed = false"
    >
      <PannaIcon class="collapsed-icon" />
      <span class="collapsed-label">Panna</span>
    </button>
  </aside>
</template>

<style scoped lang="scss">
.panna-rail {
  flex-shrink: 0;
  height: 100vh;
  position: relative;
  z-index: 15;
}

// 展开态面板
.panna-panel {
  width: 360px;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: var(--app-panel-bg);
  box-shadow: var(--app-shadow-sm);
}

.panna-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  background: var(--app-panel-bg);

  .brand {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .brand-icon {
    width: 22px;
    height: 22px;
    color: var(--app-primary);
  }

  .brand-name {
    font-size: 1.14em;
    font-weight: 600;
    color: var(--app-text-1);
    line-height: 1.2;
  }

  .brand-sub {
    font-size: 0.79em;
    color: var(--app-text-3);
    margin-top: 1px;
  }
}

.icon-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  color: var(--app-text-3);
  border-radius: var(--app-radius);
  cursor: pointer;
  transition: background 0.15s, color 0.15s;

  &:hover {
    background: var(--app-inset-bg);
    color: var(--app-text-1);
  }
}

// 模式切换
.mode-switch {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 4px;
  padding: 8px 12px;
  background: var(--app-panel-bg);
}

.mode-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 8px 4px;
  border: none;
  background: transparent;
  color: var(--app-text-2);
  border-radius: calc(var(--app-radius) - 4px);
  cursor: pointer;
  transition: background 0.15s, color 0.15s;

  &:hover {
    background: var(--app-inset-bg);
    color: var(--app-text-1);
  }

  &.active {
    background: color-mix(in srgb, var(--app-primary) 10%, transparent);
    color: var(--app-primary);
  }

  .mode-icon {
    width: 20px;
    height: 20px;
  }

  .mode-label {
    font-size: 0.79em;
    line-height: 1;
  }
}

// 内容区
.panna-body {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  padding: 8px 16px 12px;
  overflow: hidden;
}

.mode-hint {
  font-size: 0.86em;
  color: var(--app-text-3);
  padding: 8px 10px;
  background: var(--app-inset-bg);
  border-radius: calc(var(--app-radius) - 4px);
  margin-bottom: 8px;
}

.message-list {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.empty-hint {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  color: var(--app-text-3);

  .empty-icon {
    width: 36px;
    height: 36px;
    color: var(--app-text-3);
    opacity: 0.6;
  }

  .empty-text {
    font-size: 0.93em;
    color: var(--app-text-2);
    font-weight: 500;
  }

  .empty-sub {
    font-size: 0.79em;
  }
}

// 输入区
.panna-footer {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  padding: 12px 16px 14px;
  background: var(--app-panel-bg);
}

.input-area {
  flex: 1;
  resize: none;
  border: none;
  background: var(--app-inset-bg);
  border-radius: calc(var(--app-radius) - 4px);
  padding: 8px 12px;
  font-family: inherit;
  font-size: 0.93em;
  color: var(--app-text-1);
  line-height: 1.5;
  outline: none;
  transition: box-shadow 0.15s;

  &:focus {
    box-shadow: 0 0 0 1.5px var(--app-primary);
  }

  &::placeholder {
    color: var(--app-text-3);
  }
}

.send-btn {
  flex-shrink: 0;
  padding: 8px 16px;
  border: none;
  background: var(--app-primary);
  color: #fff;
  border-radius: calc(var(--app-radius) - 2px);
  font-size: 0.86em;
  cursor: pointer;
  transition: background 0.15s, transform 0.1s;

  &:hover {
    background: color-mix(in srgb, var(--app-primary) 88%, #fff);
  }

  &:active {
    transform: translateY(1px);
  }
}

// 折叠态窄条
.panna-collapsed {
  width: 48px;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  border: none;
  background: var(--app-panel-bg);
  color: var(--app-text-2);
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
  writing-mode: vertical-rl;

  &:hover {
    background: var(--app-inset-bg);
    color: var(--app-primary);
  }

  .collapsed-icon {
    width: 22px;
    height: 22px;
  }

  .collapsed-label {
    font-size: 0.86em;
    font-weight: 500;
    letter-spacing: 2px;
  }
}
</style>
