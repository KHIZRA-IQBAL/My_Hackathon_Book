# Integrating ChatBot with Docusaurus

Step-by-step guide to add the Physical AI chatbot to your Docusaurus site.

## Prerequisites

- Docusaurus site set up in `../book/`
- Chatbot backend running (locally or deployed)
- ChatBot React component created in `../book/src/components/ChatBot/`

## Step 1: Add ChatBot to Layout

### Option A: Global Integration (Recommended)

Add the chatbot to every page using a custom layout wrapper.

**Create** `book/src/theme/Root.tsx`:

```typescript
import React from 'react';
import ChatBot from '@site/src/components/ChatBot';

// Default implementation, that you can customize
export default function Root({children}) {
  return (
    <>
      {children}
      <ChatBot />
    </>
  );
}
```

### Option B: Specific Pages Only

Import the ChatBot component on specific pages:

```mdx
---
title: Physical AI Introduction
---

import ChatBot from '@site/src/components/ChatBot';

# Physical AI Introduction

Your content here...

<ChatBot />
```

## Step 2: Configure API URL

### Development Mode

For local testing, the chatbot will use `http://localhost:8000` by default.

### Production Mode

Update `book/docusaurus.config.ts`:

```typescript
const config: Config = {
  // ... other config

  customFields: {
    chatbotApiUrl: process.env.CHATBOT_API_URL || 'https://your-app.railway.app',
  },

  // ... rest of config
};
```

Then update `book/src/components/ChatBot/index.tsx`:

```typescript
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export default function ChatBot(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  const CHATBOT_API_URL = (siteConfig.customFields?.chatbotApiUrl as string) ||
                           'http://localhost:8000';

  // ... rest of component
}
```

## Step 3: Add Environment Variables

Create `book/.env.local`:

```env
REACT_APP_CHATBOT_API_URL=http://localhost:8000
```

For production (GitHub Pages), add to deployment workflow.

## Step 4: Test Locally

```bash
cd book

# Start Docusaurus
npm run start

# In another terminal, start the backend
cd ../chatbot-backend
uvicorn main:app --reload
```

Visit `http://localhost:3000` and click the chatbot button (💬) in the bottom right.

**Test checklist:**
- [ ] Chatbot button appears
- [ ] Clicking opens chat window
- [ ] Can send messages
- [ ] Receives responses
- [ ] Sources are clickable
- [ ] Week filter works
- [ ] "Clear" button works
- [ ] Mobile responsive

## Step 5: Customize Styling (Optional)

### Change Colors

Edit `book/src/components/ChatBot/styles.module.css`:

```css
/* Change primary gradient */
.chatButton {
  background: linear-gradient(135deg, #your-color1 0%, #your-color2 100%);
}

/* Change chat header */
.chatHeader {
  background: linear-gradient(135deg, #your-color1 0%, #your-color2 100%);
}
```

### Change Position

```css
.chatButton {
  bottom: 24px;
  right: 24px; /* Change to left: 24px for left side */
}
```

### Change Size

```css
.chatWindow {
  width: 500px; /* Wider window */
  height: 700px; /* Taller window */
}
```

## Step 6: Advanced Features

### Feature 1: Selected Text Query

Already implemented! Users can:
1. Select text on any page
2. Click "Ask about this" button
3. Chatbot opens with pre-filled query

### Feature 2: Context-Aware Queries

Auto-detect current week and filter responses:

```typescript
// In ChatBot/index.tsx

useEffect(() => {
  // Detect current page's week from URL
  const path = window.location.pathname;
  const weekMatch = path.match(/week-(\d{2}-\d{2})/);

  if (weekMatch) {
    setWeekFilter(weekMatch[0]); // e.g., "week-01-02"
  }
}, []);
```

### Feature 3: Keyboard Shortcuts

Add keyboard support:

```typescript
useEffect(() => {
  const handleKeyPress = (e: KeyboardEvent) => {
    // Ctrl+K or Cmd+K to toggle chatbot
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      setIsOpen(prev => !prev);
    }
  };

  document.addEventListener('keydown', handleKeyPress);
  return () => document.removeEventListener('keydown', handleKeyPress);
}, []);
```

### Feature 4: Conversation Persistence

Save conversation to localStorage:

```typescript
// Save messages
useEffect(() => {
  localStorage.setItem('chatHistory', JSON.stringify(messages));
}, [messages]);

// Load messages on mount
useEffect(() => {
  const saved = localStorage.getItem('chatHistory');
  if (saved) {
    setMessages(JSON.parse(saved));
  }
}, []);
```

### Feature 5: Analytics Integration

Track chatbot usage with Google Analytics:

```typescript
const handleSubmit = async (e: React.FormEvent) => {
  // ... existing code

  // Track question asked
  if (window.gtag) {
    window.gtag('event', 'chatbot_question', {
      question: inputValue,
      week_filter: weekFilter || 'all'
    });
  }
};
```

## Step 7: Deploy to GitHub Pages

### Update Build Command

In `book/package.json`:

```json
{
  "scripts": {
    "build": "CHATBOT_API_URL=https://your-app.railway.app docusaurus build"
  }
}
```

### GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: 18

      - name: Install dependencies
        run: cd book && npm ci

      - name: Build
        env:
          CHATBOT_API_URL: ${{ secrets.CHATBOT_API_URL }}
        run: cd book && npm run build

      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./book/build
```

Add `CHATBOT_API_URL` to GitHub Secrets:
1. Go to Settings → Secrets → Actions
2. Add new secret: `CHATBOT_API_URL` = `https://your-app.railway.app`

## Step 8: Mobile Optimization

The ChatBot component is already mobile-responsive, but you can improve it:

### Full-Screen on Mobile

```css
@media (max-width: 768px) {
  .chatWindow {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100vw;
    height: 100vh;
    border-radius: 0;
  }
}
```

### Disable Zoom on Input Focus

In `book/static/index.html`:

```html
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
```

## Step 9: Accessibility

Ensure the chatbot is accessible:

### Keyboard Navigation

Already implemented:
- Tab to navigate
- Enter to send messages
- Escape to close (add this):

```typescript
useEffect(() => {
  const handleEscape = (e: KeyboardEvent) => {
    if (e.key === 'Escape' && isOpen) {
      setIsOpen(false);
    }
  };

  document.addEventListener('keydown', handleEscape);
  return () => document.removeEventListener('keydown', handleEscape);
}, [isOpen]);
```

### Screen Reader Support

Add ARIA labels (already included in component):
- `aria-label` on buttons
- `role="dialog"` on chat window
- `aria-live="polite"` for new messages

## Step 10: Performance Optimization

### Lazy Load ChatBot

Only load when needed:

```typescript
// In Root.tsx
import React, { lazy, Suspense } from 'react';

const ChatBot = lazy(() => import('@site/src/components/ChatBot'));

export default function Root({children}) {
  return (
    <>
      {children}
      <Suspense fallback={null}>
        <ChatBot />
      </Suspense>
    </>
  );
}
```

### Debounce Typing

Prevent API calls on every keystroke:

```typescript
import { debounce } from 'lodash';

const debouncedSubmit = debounce(handleSubmit, 300);
```

## Troubleshooting

### ChatBot button doesn't appear

**Check**:
1. Component imported correctly in `Root.tsx`
2. CSS module imported in component
3. No console errors
4. Component is exported as default

### API connection fails

**Check**:
1. Backend is running
2. CORS configured correctly in backend
3. API URL is correct
4. Network tab shows request details

### Styling issues

**Check**:
1. CSS modules enabled in Docusaurus (default)
2. No conflicting global styles
3. Dark mode support works
4. Mobile styles applied

### Performance issues

**Solutions**:
1. Lazy load component
2. Implement caching for common questions
3. Reduce bundle size with code splitting
4. Use production build: `npm run build`

## Examples

### Minimal Integration

```typescript
// Root.tsx
import React from 'react';
import ChatBot from '@site/src/components/ChatBot';

export default function Root({children}) {
  return (
    <>
      {children}
      <ChatBot />
    </>
  );
}
```

### Advanced Integration with Analytics

```typescript
import React, { useEffect } from 'react';
import ChatBot from '@site/src/components/ChatBot';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export default function Root({children}) {
  const {siteConfig} = useDocusaurusContext();

  useEffect(() => {
    // Track chatbot availability
    if (window.gtag) {
      window.gtag('event', 'chatbot_loaded');
    }
  }, []);

  return (
    <>
      {children}
      <ChatBot />
    </>
  );
}
```

## Testing Checklist

- [ ] ChatBot appears on all pages
- [ ] Can send and receive messages
- [ ] Sources are clickable and correct
- [ ] Week filter works
- [ ] Clear conversation works
- [ ] Feedback buttons work
- [ ] Loading state shows
- [ ] Error messages display
- [ ] Mobile responsive
- [ ] Dark mode works
- [ ] Keyboard accessible
- [ ] No console errors
- [ ] Performance acceptable (<100ms load)

## Next Steps

1. **Collect Feedback**: Monitor `/feedback` endpoint
2. **Analyze Usage**: Check `/stats` for popular questions
3. **Iterate**: Improve responses based on feedback
4. **Expand**: Add more weeks of content
5. **Optimize**: Cache common questions

## Resources

- [Docusaurus Docs](https://docusaurus.io/docs)
- [React Docs](https://react.dev)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Qdrant Docs](https://qdrant.tech/documentation)
