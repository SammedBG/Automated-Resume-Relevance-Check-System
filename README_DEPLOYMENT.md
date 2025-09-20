# 🚀 Resume Relevance Check System - Deployment Guide

## 📋 Prerequisites

1. **GitHub Account** - For hosting your code
2. **Streamlit Cloud Account** - For free deployment (optional)
3. **Python 3.8+** - For local development

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Recommended - FREE)

**Steps:**
1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `streamlit_app.py`
   - Click "Deploy"

**Benefits:**
- ✅ Free hosting
- ✅ Automatic updates on git push
- ✅ Custom domain support
- ✅ Built-in analytics

### Option 2: Heroku

**Steps:**
1. **Install Heroku CLI**
2. **Create Procfile:**
   ```bash
   echo "web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile
   ```
3. **Deploy:**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Option 3: Docker Deployment

**Steps:**
1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements_deploy.txt .
   RUN pip install -r requirements_deploy.txt
   COPY . .
   EXPOSE 8501
   CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```
2. **Build and run:**
   ```bash
   docker build -t resume-checker .
   docker run -p 8501:8501 resume-checker
   ```

### Option 4: AWS/GCP/Azure

**For production deployments:**
- Use container services (ECS, Cloud Run, Container Instances)
- Set up load balancers
- Configure auto-scaling
- Use managed databases

## 🔧 Environment Variables

Create a `.env` file for sensitive data:
```env
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
SECRET_KEY=your_secret_key
```

## 📊 Performance Optimization

1. **Enable caching:**
   ```python
   @st.cache_data
   def load_model():
       return ResumeProcessor()
   ```

2. **Use session state:**
   ```python
   if 'processor' not in st.session_state:
       st.session_state.processor = ResumeProcessor()
   ```

3. **Optimize file uploads:**
   - Limit file sizes
   - Use progress bars
   - Implement batch processing

## 🛡️ Security Considerations

1. **API Keys:**
   - Never commit API keys to git
   - Use environment variables
   - Rotate keys regularly

2. **File Uploads:**
   - Validate file types
   - Scan for malware
   - Limit file sizes

3. **Rate Limiting:**
   - Implement request limits
   - Use authentication if needed

## 📈 Monitoring & Analytics

1. **Streamlit Analytics:**
   - Built-in usage analytics
   - Performance metrics
   - Error tracking

2. **Custom Monitoring:**
   - Add logging
   - Set up alerts
   - Monitor resource usage

## 🔄 CI/CD Pipeline

**GitHub Actions example:**
```yaml
name: Deploy to Streamlit Cloud
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Streamlit Cloud
        run: echo "Deployment triggered by push to main"
```

## 🆘 Troubleshooting

**Common Issues:**
1. **Import errors:** Check requirements.txt
2. **Memory issues:** Optimize model loading
3. **Timeout errors:** Increase timeout settings
4. **File upload issues:** Check file size limits

**Debug mode:**
```bash
streamlit run streamlit_app.py --logger.level=debug
```

## 📞 Support

- Check Streamlit documentation
- Review error logs
- Test locally first
- Use community forums

---

**Ready to deploy? Start with Streamlit Cloud for the easiest setup!** 🚀
