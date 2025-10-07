// Test GLM 4.5 API integration
require('dotenv').config();

async function testGLMAPI() {
    const apiKey = process.env.GLM_API_KEY;
    const baseUrl = process.env.GLM_BASE_URL;
    
    console.log('Testing GLM 4.5 API...');
    console.log('API Key:', apiKey ? `${apiKey.substring(0, 10)}...${apiKey.slice(-10)}` : 'Not found');
    console.log('API Key Length:', apiKey ? apiKey.length : 'Not found');
    console.log('Base URL:', baseUrl);
    
    // Try different model names
    const models = ['glm-4', 'glm-4-plus', 'glm-4-air', 'glm-4-airx', 'glm-4-long', 'glm-4-flashx'];
    
    for (const model of models) {
        console.log(`\nTrying model: ${model}`);
        try {
            const response = await fetch(`${baseUrl}/chat/completions`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${apiKey}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    model: model,
                    messages: [
                        {
                            role: 'user',
                            content: 'Hello! This is a test message.'
                        }
                    ],
                    max_tokens: 50
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                console.log(`✅ ${model} - API Test Successful!`);
                console.log('Response:', data.choices[0].message.content);
                return; // Stop testing once we find a working model
            } else {
                console.log(`❌ ${model} - Error:`, data.error?.message || data);
            }
        } catch (error) {
            console.log(`❌ ${model} - Connection Error:`, error.message);
        }
    }
}

testGLMAPI();