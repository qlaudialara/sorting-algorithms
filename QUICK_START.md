# Quick Start - Push to GitHub

## ⚡ 3 Simple Steps

### Step 1: Create Repository on GitHub
- Go to: https://github.com/new
- **Repository name**: `sorting-algorithms-experiment`
- Click **Create repository**
- Done!

### Step 2: Get Your Personal Access Token
- Go to: https://github.com/settings/tokens
- Click **Generate new token** → **Generate new token (classic)**
- Fill in:
  - **Token name**: `sorting-experiment`
  - **Expiration**: 90 days
  - **Scopes**: Check `repo`
- Click **Generate token**
- **Copy the token** (shown only once!)

### Step 3: Push Your Code

**Option A - Use the Script:**
```bash
cd /Users/qlaudia/sorting-experiment
bash push-to-github.sh
```

**Option B - Manual Command:**
```bash
cd /Users/qlaudia/sorting-experiment
git push -u origin main
```

When prompted:
- **Username**: `qlaudialara`
- **Password**: Paste your Personal Access Token

## ✅ That's it!

Your repository will be at:
```
https://github.com/qlaudialara/sorting-algorithms-experiment
```

## 📋 What's Included

```
sorting-experiment/
├── README.md                    # Main documentation
├── LICENSE                      # MIT License
├── requirements.txt             # Dependencies
├── main.py                      # Full experiment (1000+ configs)
├── quick_test.py                # Quick validation (2-3 min)
│
├── algorithms/                  # 10 sorting algorithms
├── data_generation/             # Dataset generation
├── experiments/                 # Experiment runner
├── visualization/               # Plotting module
│
└── push-to-github.sh            # This push script
```

## 🚀 After Push

Your code is on GitHub! Now you can:

1. **Make changes locally**
   ```bash
   git add .
   git commit -m "Your message"
   git push
   ```

2. **Run experiments**
   ```bash
   python3 main.py              # Full run (~30-60 min)
   python3 quick_test.py        # Quick test (~2-3 min)
   ```

3. **Share with others**
   - Copy the URL: `https://github.com/qlaudialara/sorting-algorithms-experiment`
   - People can clone it: `git clone https://github.com/qlaudialara/sorting-algorithms-experiment`

## 💡 Troubleshooting

**"fatal: 'origin' does not appear to be a 'git' repository"**
- You're in the wrong folder
- Make sure you're in: `/Users/qlaudia/sorting-experiment`

**"Authentication failed"**
- Check your PAT is correct
- Make sure you used `repo` scope
- Try creating a new PAT

**"Repository already exists"**
- Your repo is already on GitHub
- Use: `git push -f origin main` to overwrite

## 📞 Need Help?

Check Git status:
```bash
cd /Users/qlaudia/sorting-experiment
git status
git log --oneline
```

View this setup again:
```bash
cat QUICK_START.md
```

---

**Ready? Run the push script now!** 🚀
