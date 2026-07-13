import { useState } from 'react';
import type { Post } from '../App';
import { Copy, MoreVertical, GripVertical, RotateCcw, Maximize2 } from 'lucide-react';

interface PostCardProps {
  post: Post;
  onUpdate: (post: Post) => void;
  onOpenModal: () => void;
  innerRef?: React.Ref<HTMLDivElement>;
  draggableProps?: any;
  dragHandleProps?: any;
  isDragging?: boolean;
  isVisualView?: boolean;
}

export default function PostCard({
  post, onUpdate, onOpenModal,
  innerRef, draggableProps, dragHandleProps, isDragging, isVisualView
}: PostCardProps) {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [menuOpen, setMenuOpen] = useState(false);

  const totalSlides = post.visual_content?.length || 1;

  const prevSlide = (e: React.MouseEvent) => {
    e.stopPropagation();
    setCurrentSlide(s => Math.max(0, s - 1));
  };
  const nextSlide = (e: React.MouseEvent) => {
    e.stopPropagation();
    setCurrentSlide(s => Math.min(totalSlides - 1, s + 1));
  };

  const updateField = <K extends keyof Post>(key: K, value: Post[K]) => {
    onUpdate({ ...post, [key]: value });
  };

  const handleCopy = (e: React.MouseEvent, text: string) => {
    e.stopPropagation();
    navigator.clipboard.writeText(text);
  };

  const slideContent = post.visual_content?.[currentSlide]?.text || 'Sin contenido visual';
  const campaignClass = post.campaign.includes('Legal') ? 'campaign-legal' : 'campaign-tech';

  return (
    <div
      className={`card ${isDragging ? 'is-dragging' : ''}`}
      ref={innerRef}
      {...draggableProps}
    >
      <div className={`status-indicator status-${post.status}`} title={post.status} />

      {/* ── Card Header ── */}
      <div className="card-header">
        <div className="header-tags">
          <div {...dragHandleProps} className="drag-handle">
            <GripVertical size={18} />
          </div>
          <span className="post-id-badge">{post.id}</span>
          <select
            className="type-select"
            value={post.type}
            onChange={(e) => updateField('type', e.target.value as Post['type'])}
          >
            <option value="image">Image</option>
            <option value="carousel">Carousel</option>
            <option value="video">Video</option>
          </select>
          <span className={`campaign-tag ${campaignClass}`}>
            {post.campaign}
          </span>
        </div>

        <div style={{ position: 'relative' }}>
          <button className="menu-btn" onClick={() => setMenuOpen(!menuOpen)}>
            <MoreVertical size={20} />
          </button>

          {menuOpen && (
            <div className="dropdown-menu">
              {post.status === 'discarded' ? (
                <button className="dropdown-item" onClick={() => { updateField('status', 'pending'); setMenuOpen(false); }}>
                  <RotateCcw size={14} style={{ display: 'inline', marginRight: '6px' }} /> Restaurar
                </button>
              ) : (
                <>
                  <button className="dropdown-item" onClick={() => { updateField('status', 'approved'); setMenuOpen(false); }}>
                    ✅ Aprobar
                  </button>
                  <button className="dropdown-item" onClick={() => { updateField('status', 'discarded'); setMenuOpen(false); }}>
                    ❌ Descartar
                  </button>
                </>
              )}
              <button className="dropdown-item" onClick={() => { onOpenModal(); setMenuOpen(false); }}>
                <Maximize2 size={14} style={{ display: 'inline', marginRight: '6px' }} /> Ver detalle
              </button>
            </div>
          )}
        </div>
      </div>

      {/* ── Visual Preview (clickable → opens modal) ── */}
      <div className="visual-preview" onClick={onOpenModal}>
        {/* Slide counter */}
        {post.type === 'carousel' && totalSlides > 1 && (
          <span className="slide-indicator">{currentSlide + 1} / {totalSlides}</span>
        )}

        {/* Prev/Next nav */}
        {post.type === 'carousel' && currentSlide > 0 && (
          <button className="slide-nav slide-prev" onClick={prevSlide}>‹</button>
        )}

        <div className="slide-content" style={{ padding: isVisualView ? 0 : '1.5rem', overflow: 'hidden' }}>
          {isVisualView && post.images && post.images[currentSlide] ? (
            <img 
              src={post.images[currentSlide]} 
              alt={`Slide ${currentSlide + 1}`} 
              style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }} 
            />
          ) : (
            <p>{slideContent}</p>
          )}
        </div>

        {post.type === 'carousel' && currentSlide < totalSlides - 1 && (
          <button className="slide-nav slide-next" onClick={nextSlide}>›</button>
        )}

        {/* Dots indicator (Instagram style) */}
        {post.type === 'carousel' && totalSlides > 1 && (
          <div className="card-slide-dots">
            {post.visual_content?.map((_, i) => (
              <span key={i} className={`card-slide-dot ${i === currentSlide ? 'active' : ''}`} />
            ))}
          </div>
        )}

        {/* Expand hint shown on hover */}
        <div className="preview-expand-hint">
          <Maximize2 size={13} />
        </div>
      </div>

      {/* ── Card Body ── */}
      <div className="card-body">
        <button
          className="btn btn-copy"
          onClick={(e) => handleCopy(e, slideContent)}
        >
          <Copy size={16} /> Copiar Texto / Guion
        </button>

        <div className="copy-text">
          {post.copy}
        </div>

        <button
          className="btn btn-copy"
          onClick={(e) => handleCopy(e, post.copy)}
        >
          <Copy size={16} /> Copiar Copy
        </button>

        {post.status !== 'approved' && (
          <div style={{ marginTop: '1rem' }}>
            <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', display: 'block', marginBottom: '0.4rem' }}>
              Feedback
            </label>
            <textarea
              className="feedback-input"
              rows={2}
              placeholder="¿Qué falló?"
              value={post.feedback || ''}
              onChange={(e) => updateField('feedback', e.target.value)}
              onClick={e => e.stopPropagation()}
            />
          </div>
        )}
      </div>
    </div>
  );
}
