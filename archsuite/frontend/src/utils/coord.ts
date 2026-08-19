// CGCS2000 高斯-克吕格 3 度带 坐标转换工具
// 椭球参数采用 CGCS2000（与 WGS84 在工程精度内一致，差异厘米级）
// 公式为标准高斯-克吕格正反算级数展开，工程精度优于 0.1m

// CGCS2000 椭球参数
const A_SEMI = 6378137.0 // 长半轴 (m)
const INV_F = 298.257222101 // 扁率倒数
const F = 1 / INV_F
const E2 = 2 * F - F * F // 第一偏心率平方
const E2P = E2 / (1 - E2) // 第二偏心率平方 e'²

const PI = Math.PI
const DEG = PI / 180

// 3 度带带号：自动按经度选择最近的中央子午线
export function calcZone3(lng: number): number {
  // 带号 = round(lng / 3)，向最近整数取整
  return Math.round(lng / 3)
}

export interface GaussCoord {
  X: number // 北坐标 (m)，即 Northing
  Y: number // 东坐标 (m)，含带号 + 500000 偏移，即 Easting
  zone: number // 3 度带带号
  L0: number // 中央子午线经度 (度)
}

// 经纬度（WGS84/CGCS2000，度） -> 3 度带高斯-克吕格 XY
export function lngLatToGauss3(lng: number, lat: number): GaussCoord {
  const zone = calcZone3(lng)
  const L0 = zone * 3
  const l = (lng - L0) * DEG // 经差弧度
  const B = lat * DEG // 纬度弧度

  const sinB = Math.sin(B)
  const cosB = Math.cos(B)
  const tanB = Math.tan(B)
  const sin2B = Math.sin(2 * B)
  const sin4B = Math.sin(4 * B)
  const sin6B = Math.sin(6 * B)

  // 卯酉圈曲率半径
  const N = A_SEMI / Math.sqrt(1 - E2 * sinB * sinB)
  const T = tanB * tanB
  const C = E2P * cosB * cosB
  const AA = cosB * l // 记为 a，避免与长半轴混淆

  // 子午线弧长 M（赤道到 B）
  const M =
    A_SEMI *
    ((1 - E2 / 4 - (3 * E2 * E2) / 64 - (5 * E2 * E2 * E2) / 256) * B -
      ((3 * E2) / 8 + (3 * E2 * E2) / 32 + (45 * E2 * E2 * E2) / 1024) * sin2B +
      ((15 * E2 * E2) / 256 + (45 * E2 * E2 * E2) / 1024) * sin4B -
      ((35 * E2 * E2 * E2) / 3072) * sin6B)

  const A2 = AA * AA
  const A3 = A2 * AA
  const A4 = A2 * A2
  const A5 = A4 * AA
  const A6 = A3 * A3

  const X =
    M +
    N *
      tanB *
      (A2 / 2 +
        ((5 - T + 9 * C + 4 * C * C) * A4) / 24 +
        ((61 - 58 * T + T * T + 600 * C - 330 * E2P) * A6) / 720)
  let Y =
    N *
    (AA +
      ((1 - T + C) * A3) / 6 +
      ((5 - 18 * T + T * T + 72 * C - 58 * E2P) * A5) / 120)

  // Y 加 500000 + 带号*1000000（中国高斯坐标惯例：带号在前）
  Y = Y + 500000 + zone * 1000000

  return { X, Y, zone, L0 }
}

export interface LngLat {
  lng: number
  lat: number
  zone: number
  L0: number
}

// 3 度带高斯-克吕格 XY -> 经纬度
// zoneHint: 若 Y 未带带号，必须提供；若 Y 含带号会自动解析
export function gauss3ToLngLat(X: number, Y: number, zoneHint?: number): LngLat {
  let zone: number
  let yReal: number
  if (zoneHint != null) {
    zone = zoneHint
    yReal = Y - 500000 - zone * 1000000
  } else if (Y > 1000000) {
    // Y 含带号
    zone = Math.floor(Y / 1000000)
    yReal = Y - 500000 - zone * 1000000
  } else {
    // 无带号且未提供 hint，按 X 推算近似带号
    zone = Math.round(X / 100000) // 粗略，调用方应提供 zoneHint
    yReal = Y - 500000
  }
  const L0 = zone * 3

  // 迭代求底点纬度 Bf（M(Bf) = X）
  // 初值：X / (近似子午弧长系数)
  let Bf = X / (A_SEMI * (1 - E2 / 4))
  for (let i = 0; i < 8; i++) {
    const sBf = Math.sin(Bf)
    const sin2Bf = Math.sin(2 * Bf)
    const sin4Bf = Math.sin(4 * Bf)
    const sin6Bf = Math.sin(6 * Bf)
    const Mf =
      A_SEMI *
      ((1 - E2 / 4 - (3 * E2 * E2) / 64 - (5 * E2 * E2 * E2) / 256) * Bf -
        ((3 * E2) / 8 + (3 * E2 * E2) / 32 + (45 * E2 * E2 * E2) / 1024) * sin2Bf +
        ((15 * E2 * E2) / 256 + (45 * E2 * E2 * E2) / 1024) * sin4Bf -
        ((35 * E2 * E2 * E2) / 3072) * sin6Bf)
    // 子午弧长对 B 的导数（M'）
    const dM =
      A_SEMI *
      (1 - E2 / 4 - (3 * E2 * E2) / 64 - (5 * E2 * E2 * E2) / 256) *
      (1 - E2 * sBf * sBf) // 近似
    const delta = (X - Mf) / dM
    Bf = Bf + delta
    if (Math.abs(delta) < 1e-11) break
  }

  const sinBf = Math.sin(Bf)
  const cosBf = Math.cos(Bf)
  const tanBf = Math.tan(Bf)
  const Nf = A_SEMI / Math.sqrt(1 - E2 * sinBf * sinBf)
  const Tf = tanBf * tanBf
  const Cf = E2P * cosBf * cosBf
  const Rf = (A_SEMI * (1 - E2)) / Math.pow(1 - E2 * sinBf * sinBf, 1.5)
  const D = yReal / Nf

  const D2 = D * D
  const D3 = D2 * D
  const D4 = D2 * D2
  const D5 = D4 * D
  const D6 = D3 * D3
  const D7 = D6 * D

  // 纬度 B
  const B =
    Bf -
    (Nf * tanBf / Rf) *
      (D2 / 2 -
        (5 + 3 * Tf + 6 * Cf - 6 * E2P * Cf * Cf - 3 * E2P * Tf) * D4 / 24 +
        (61 + 90 * Tf + 298 * Cf + 45 * Tf * Tf - 3 * Cf * Cf - 252 * E2P) * D6 / 720)

  // 经差 l
  const l =
    (D -
      (1 + 2 * Tf + Cf) * D3 / 6 +
      (5 - 2 * Cf + 28 * Tf - 3 * Cf * Cf + 8 * E2P + 24 * Tf * Tf) * D5 / 120 +
      (61 - 58 * Tf + Cf * Cf + 270 * Tf * (4 - E2P) - 330 * E2P * Tf) * D7 / 5040) /
    cosBf

  void D7 // 占位避免 lint
  const lat = B / DEG
  const lng = L0 + l / DEG

  return { lng, lat, zone, L0 }
}

// 解析红线坐标表格（CSV / TSV / 粘贴文本）
// 支持表头：序号,X,Y 或 point,x,y 或 名称,北,东 等
// 返回 CGCS2000 XY 点列表
export interface RedPoint {
  seq: number
  name: string
  x: number // 北
  y: number // 东
}

export interface ParseResult {
  ok: boolean
  points: RedPoint[]
  zone?: number
  message: string
}

// 从一行文本识别 X / Y 两列
function parseRow(tokens: string[]): { x: number; y: number; name: string } | null {
  if (tokens.length < 2) return null
  // 找两个可解析为数字的列
  const nums: number[] = []
  let name = ''
  for (const t of tokens) {
    const v = Number(t.trim())
    if (!Number.isNaN(v) && t.trim() !== '') nums.push(v)
    else name = (name + ' ' + t.trim()).trim()
  }
  if (nums.length < 2) return null
  // 约定：第一数为 X(北)，第二数为 Y(东)。若检测到 Y 含带号(>1e6)则交换更稳
  let x = nums[0]
  let y = nums[1]
  // 若第一个数明显是带号 Y（>1e6）且第二个数较小，则交换
  if (x > 1000000 && y < 1000000) {
    ;[x, y] = [y, x]
  }
  return { x, y, name }
}

export function parseRedLineText(text: string): ParseResult {
  const lines = text
    .split(/\r?\n/)
    .map((l) => l.trim())
    .filter((l) => l.length > 0)
  if (!lines.length) return { ok: false, points: [], message: '内容为空' }

  // 检测分隔符
  const sep = lines[0].includes('\t') ? '\t' : lines[0].includes(',') ? ',' : /\s+/
  const rows = lines.map((l) => (typeof sep === 'string' ? l.split(sep) : l.split(sep)))

  // 跳过表头：首行若含非数字列则视为表头
  let startIdx = 0
  const firstRowNums = rows[0].map((t) => Number(t.trim())).filter((n) => !Number.isNaN(n) && n !== 0)
  if (firstRowNums.length < 2) startIdx = 1

  const points: RedPoint[] = []
  let detectedZone: number | undefined
  for (let i = startIdx; i < rows.length; i++) {
    const parsed = parseRow(rows[i])
    if (!parsed) continue
    // 推断带号
    if (detectedZone == null && parsed.y > 1000000) {
      detectedZone = Math.floor(parsed.y / 1000000)
    }
    points.push({ seq: points.length + 1, name: parsed.name || `P${points.length + 1}`, x: parsed.x, y: parsed.y })
  }

  if (!points.length) return { ok: false, points: [], message: '未识别到有效坐标行' }
  return { ok: true, points, zone: detectedZone, message: `识别到 ${points.length} 个坐标点` }
}
