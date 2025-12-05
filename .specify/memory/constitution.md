## Project: Physical AI & Humanoid Robotics Textbook

**Project Type**: AI-native educational textbook with embedded RAG chatbot  
**Hackathon**: Panaversity Hackathon I  
**Deadline**: December 7, 2025, 12:00 PM  
**Author**: KHIZRA IQBAL  
**Repository**: https://github.com/KHIZRA-IQBAL/My_Hackathon_Book

---

## Core Principles

### 1. Technical Accuracy Through Verification
- All robotics concepts verified against official documentation
- ROS 2 information cross-checked with docs.ros.org
- NVIDIA Isaac details from developer.nvidia.com/isaac
- Gazebo specifications from gazebosim.org
- No assumptions without source verification

### 2. Clarity for Target Audience
- Target: Students with Python programming and basic AI/ML knowledge
- Progressive difficulty: beginner → intermediate → advanced
- Practical examples in every chapter
- Clear explanations before technical depth
- Avoid jargon without definition

### 3. Reproducibility
- All code examples must be runnable
- Dependencies and versions clearly specified
- Step-by-step instructions for setup
- Expected outputs documented
- Links to official resources for further learning

### 4. Educational Rigor
- Each chapter has clear learning objectives
- Prerequisites explicitly stated
- Assessments aligned with learning outcomes
- Real-world applications demonstrated
- Industry-standard tools and practices

---

## Key Standards

### Content Standards
**Technical Claims:**
- All factual claims must link to official documentation
- Version numbers specified for all software/tools
- Hardware specifications verified against manufacturer specs
- No outdated information (must be current as of 2025)

**Citation Format:**
- Inline links to official documentation
- Reference section at end of each chapter
- Format: [Source Name](URL) - Description
- Example: [ROS 2 Humble Docs](https://docs.ros.org/en/humble/) - Official ROS 2 Documentation

**Source Quality Requirements:**
- Minimum 70% from official documentation
- Remaining 30% from reputable sources (research papers, industry blogs)
- Acceptable sources: ROS.org, NVIDIA Developer, Gazebo, IEEE papers, ArXiv
- Avoid: Medium blogs, Reddit posts, outdated tutorials

**Code Quality:**
- All Python code follows PEP 8 style guide
- Type hints included for functions
- Comments explain the "why", not the "what"
- Tested and functional (no pseudo-code without clear marking)
- Syntax highlighting properly configured

**Plagiarism:**
- 0% tolerance for copied content
- All borrowed concepts properly attributed
- Original explanations and examples
- Paraphrasing with citation where needed

**Writing Clarity:**
- Active voice preferred over passive
- Short sentences (max 25 words average)
- Technical terms defined on first use
- Clear section headings and subheadings
- Consistent terminology throughout

### Documentation Standards

**Markdown Format:**
- Docusaurus-compatible markdown
- Front matter required:
```yaml
  ---
  sidebar_position: 1
  title: "Page Title"
  description: "Brief description for SEO"
  ---
```
- Code blocks specify language: ```python, ```bash, ```yaml
- Mermaid diagrams for architecture/flow

**File Structure:**
- Files: kebab-case (physical-ai-intro.md)
- Folders: kebab-case with context (week-01-02-physical-ai)
- Assets: descriptive names (sensor-architecture-diagram.png)

**Visual Elements:**
- Diagrams must have captions
- Images optimized (< 200KB)
- Alt text for accessibility
- Mermaid preferred over images for editable diagrams

### Code Standards

**Python:**
```python
# Type hints mandatory
def process_sensor_data(
    data: list[float], 
    threshold: float = 0.5
) -> dict[str, float]:
    """
    Process sensor readings and return filtered results.
    
    Args:
        data: Raw sensor readings
        threshold: Minimum value to include
        
    Returns:
        Dictionary with processed metrics
    """
    pass
```

**TypeScript/React:**
```typescript
// Interface for props
interface ChatBotProps {
  initialMessage?: string;
  onResponse: (response: string) => void;
}

// Functional component with hooks
export const ChatBot: React.FC<ChatBotProps> = ({ 
  initialMessage, 
  onResponse 
}) => {
  // Implementation
};
```

### Performance Standards

**Page Load:**
- Target: < 2 seconds per page
- Images lazy-loaded
- Code splitting enabled
- Lighthouse score > 90

**Chatbot Response:**
- Embedding generation: < 500ms
- Vector search: < 300ms
- LLM response: < 2 seconds
- Total end-to-end: < 3 seconds

---

## Constraints

### Time Constraints
- **Hard deadline**: November 30, 2025, 6:00 PM
- **Demo video**: Must be under 90 seconds
- **Live presentation**: By invitation only

### Resource Constraints
**Free Tier Limits:**
- Qdrant Cloud: 1GB storage
- Neon Postgres: 0.5GB storage
- OpenAI API: Budget ~$10-20 for development

**Content Scope:**
- Must cover all 13 weeks
- Each week: 4-6 pages of content
- Minimum 3 code examples per week
- Minimum 2 diagrams per week

### Technical Constraints
- Browser support: Chrome 90+, Firefox 88+, Safari 14+
- Mobile responsive: 375px minimum width
- Accessibility: WCAG 2.1 Level AA
- No external dependencies without justification

---

## Success Criteria

### Minimum Viable Product (100 points)
- [ ] All 13 weeks of content complete and deployed
- [ ] RAG chatbot functional with selected text support
- [ ] All internal links working
- [ ] No broken external links
- [ ] All code examples tested and functional
- [ ] Mermaid diagrams render correctly
- [ ] GitHub Pages deployment successful
- [ ] Demo video submitted (< 90 seconds)

### Bonus Features (150 additional points)
- [ ] **Subagents/Skills (50 pts)**: Minimum 2 subagents + 3 skills created and reused
- [ ] **Better-Auth (50 pts)**: Signup/signin with user profiling functional
- [ ] **Personalization (50 pts)**: Per-chapter content adaptation based on user profile
- [ ] **Urdu Translation (50 pts)**: Per-chapter translation with technical term handling

### Quality Metrics
- [ ] Technical accuracy: 95%+ claims verified
- [ ] Citation coverage: All technical claims cited
- [ ] Code quality: All examples tested and functional
- [ ] Performance: Page load < 2s, chatbot response < 3s
- [ ] Accessibility: Lighthouse accessibility score > 90
- [ ] Zero plagiarism detected

---

## Decision-Making Guidelines

### When to Use AI
**Use AI for:**
- Content drafting and structure
- Code example generation
- Diagram suggestions
- Explanation variations
- Translation assistance

**Always Human-Review:**
- Technical accuracy
- Code functionality
- Citation correctness
- Diagram clarity
- Assessment quality

### Trade-off Priorities
1. **Technical accuracy** > Speed (never compromise correctness)
2. **MVP completion** > Bonus features (100 points guaranteed first)
3. **Code quality** > Code quantity (working examples over many examples)
4. **Clear explanations** > Comprehensive coverage (depth over breadth)

### When Stuck
1. Check this constitution
2. Review specification for the feature
3. Consult official documentation
4. Ask Claude for guidance with context
5. Simplify scope if necessary (document for post-hackathon)

---

## Workflow Standards

### Spec-Kit Plus Process
Every feature must follow:
1. **Constitution** - Review project standards (this document)
2. **Specify** - Write detailed specification with `/sp.specify`
3. **Clarify** - Identify edge cases with `/sp.clarify`
4. **Plan** - Generate implementation plan with `/sp.plan`
5. **Tasks** - Break into atomic tasks with `/sp.tasks`
6. **Implement** - Execute with `/sp.implement`

### Git Commit Standards
**Format**: `<type>: <description>`

**Types:**
- `feat:` New feature (e.g., "feat: Add Week 1-2 Physical AI chapter")
- `fix:` Bug fix (e.g., "fix: Correct LIDAR diagram rendering")
- `docs:` Documentation (e.g., "docs: Update constitution")
- `style:` Formatting (e.g., "style: Fix markdown formatting in intro")
- `refactor:` Code restructure (e.g., "refactor: Simplify chatbot component")
- `test:` Adding tests (e.g., "test: Add chatbot response tests")
- `chore:` Maintenance (e.g., "chore: Update dependencies")

**Examples:**
```bash
git commit -m "spec: Add Week 1-2 specification"
git commit -m "feat: Implement Week 1-2 content with diagrams"
git commit -m "fix: Resolve broken links in sensor-systems.md"
```

### File Organization
```
Hackathon/
├── .specify/
│   ├── memory/constitution.md          # This file
│   ├── specs/                          # Feature specifications
│   ├── plans/                          # Implementation plans
│   └── tasks/                          # Task breakdowns
├── book/
│   └── docs/
│       ├── weeks/                      # Weekly content
│       ├── modules/                    # Module deep-dives
│       ├── hardware/                   # Hardware guides
│       └── assessments/                # Quizzes & exercises
└── chatbot-backend/                    # FastAPI + RAG
```

---

## Review & Updates

### Constitution Updates
Update this constitution when:
- Major scope changes occur
- Technical requirements change
- New constraints discovered
- Better practices identified

### Version History
- **v1.0** (2025-12-04): Initial constitution following hackathon template structure

---

## Acknowledgments
- **Template Inspiration**: Panaversity Spec-Kit Plus research paper example
- **Methodology**: AI-Native Software Development principles
- **Community**: Panaversity, ROS 2, NVIDIA Isaac communities

---

*This constitution serves as the single source of truth for all project decisions, standards, and success criteria.*

*Last Updated: December 4, 2025*  
*Author: KHIZRA IQBAL*