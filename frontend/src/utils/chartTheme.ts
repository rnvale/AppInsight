export const SIGNAL_COLORS = {
  positive: '#2E8B78',
  negative: '#C95C57',
  accent: '#E56B55',
  neutral: '#6E8190',
  neutralSoft: '#B9C5C1',
  warning: '#C99B4A',
  ink: '#16201F',
  muted: '#6E7D7A',
  faint: '#98A6A2',
  line: '#DCE6E2',
  grid: '#EDF2F0',
  panel: '#FFFFFF',
}

export const SIGNAL_SCALES = {
  positive: ['#E8F3EF', '#B5D9CE', '#6FB3A1', SIGNAL_COLORS.positive],
  negative: ['#F9EAE7', '#EBC2BC', '#D98B80', SIGNAL_COLORS.negative],
  balance: [SIGNAL_COLORS.negative, '#F7F8F6', SIGNAL_COLORS.positive],
}

export const chartBase = {
  animationDuration: 620,
  animationEasing: 'cubicOut',
  backgroundColor: 'transparent',
  textStyle: { fontFamily: 'Noto Sans SC, PingFang SC, Microsoft YaHei, sans-serif', color: SIGNAL_COLORS.ink },
}

export const chartTooltip = {
  backgroundColor: 'rgba(255, 255, 255, 0.97)',
  borderColor: SIGNAL_COLORS.line,
  borderWidth: 1,
  textStyle: { color: SIGNAL_COLORS.ink, fontSize: 12 },
  confine: true,
  padding: [10, 12],
  extraCssText: 'box-shadow: 0 14px 32px rgba(22,32,31,.14); border-radius: 8px; line-height: 1.6;',
}

export const chartAxis = {
  axisLine: { lineStyle: { color: SIGNAL_COLORS.line } },
  axisTick: { show: false },
  axisLabel: { color: SIGNAL_COLORS.muted, fontSize: 11 },
}

export const chartGrid = { left: '7%', right: '6%', top: 42, bottom: 38, containLabel: true }
