// Utility functions for the application

export const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString()
}

export const formatLocation = (latitude, longitude) => {
  if (!latitude || !longitude) return 'Unknown'
  return `${latitude.toFixed(5)}, ${longitude.toFixed(5)}`
}

export const getFraudStatus = (score, isFlagged) => {
  if (isFlagged) return { text: 'Flagged', color: 'text-rose-400' }
  if (score > 50) return { text: 'Suspicious', color: 'text-amber-400' }
  return { text: 'Normal', color: 'text-emerald-400' }
}

export const calculateStats = (attendanceData) => {
  const total = attendanceData.length
  const flagged = attendanceData.filter(item => item.is_flagged).length
  const normal = total - flagged
  const avgScore = total > 0 ? attendanceData.reduce((sum, item) => sum + item.fraud_score, 0) / total : 0

  return {
    total,
    flagged,
    normal,
    avgScore: Math.round(avgScore),
  }
}