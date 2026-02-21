# API連携パターン集

## Claude API
\`\`\`javascript
function callClaudeAPI(prompt) {
  const API_KEY = PropertiesService.getScriptProperties().getProperty('CLAUDE_API_KEY');
  const url = 'https://api.anthropic.com/v1/messages';
  
  const payload = {
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1024,
    messages: [{
      role: 'user',
      content: prompt
    }]
  };
  
  const options = {
    method: 'post',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': API_KEY,
      'anthropic-version': '2023-06-01'
    },
    payload: JSON.stringify(payload)
  };
  
  const response = UrlFetchApp.fetch(url, options);
  return JSON.parse(response.getContentText());
}
\`\`\`

## エラーハンドリング
\`\`\`javascript
function apiCallWithRetry(url, options, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = UrlFetchApp.fetch(url, options);
      return JSON.parse(response.getContentText());
    } catch(e) {
      if (i === maxRetries - 1) throw e;
      Utilities.sleep(1000 * (i + 1)); // 指数バックオフ
    }
  }
}
\`\`\`