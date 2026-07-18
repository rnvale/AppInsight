export const SIGNAL_COLORS = {
  positive: '#2E8B78',
  negative: '#C95C57',
  accent: '#E56B55',
  neutral: '#6E8190',
  warning: '#C99B4A',
  ink: '#16201F',
  muted: '#6E7D7A',
  faint: '#98A6A2',
  line: '#DCE6E2',
  grid: '#EDF2F0',
  panel: '#FFFFFF',
}

export const chartBase = {
  animationDuration: 720,
  animationEasing: 'cubicOut',
  textStyle: { fontFamily: 'Noto Sans SC, PingFang SC, Microsoft YaHei, sans-serif', color: SIGNAL_COLORS.ink },
}

export const chartTooltip = {
  backgroundColor: 'rgba(255, 255, 255, 0.97)',
  borderColor: SIGNAL_COLORS.line,
  borderWidth: 1,
  textStyle: { color: SIGNAL_COLORS.ink, fontSize: 12 },
  extraCssText: 'box-shadow: 0 10px 28px rgba(22,32,31,.12); border-radius: 7px;',
}
