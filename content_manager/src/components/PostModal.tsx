import { useState } from 'react';
import type { Post } from '../App';
import {
  Copy, X, CheckCircle, XCircle, RotateCcw,
  ChevronLeft, ChevronRight, Plus, Download
} from 'lucide-react';

interface PostModalProps {
  post: Post;
  onUpdate: (post: Post) => void;
  onClose: () => void;
}

const MAX_COPY_CHARS = 2200;
const MAX_SLIDES = 10;

export default function PostModal({ post, onUpdate, onClose }: PostModalProps) {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [editedPost, setEditedPost] = useState<Post>({
    ...post,
    visual_content: post.visual_content ? post.visual_content.map(s => ({ ...s })) : [],
  });
  const [copied, setCopied] = useState<string | null>(null);

  const slides = editedPost.visual_content || [];
  const totalSlides = slides.length;
  const copyLength = editedPost.copy?.length || 0;
  const isOverLimit = copyLength > MAX_COPY_CHARS;
  const isNearLimit = !isOverLimit && copyLength > MAX_COPY_CHARS * 0.9;

  const prevSlide = () => setCurrentSlide(s => Math.max(0, s - 1));
  const nextSlide = () => setCurrentSlide(s => Math.min(totalSlides - 1, s + 1));

  const updateSlideText = (index: number, value: string) => {
    const updated = slides.map((s, i) => i === index ? { ...s, text: value } : s);
    setEditedPost(prev => ({ ...prev, visual_content: updated }));
  };

  const addSlide = () => {
    if (totalSlides >= MAX_SLIDES) return;
    const newSlide = { slide: totalSlides + 1, text: '' };
    setEditedPost(prev => ({
      ...prev,
      visual_content: [...(prev.visual_content || []), newSlide],
    }));
    setCurrentSlide(totalSlides);
  };

  const removeSlide = (index: number) => {
    if (totalSlides <= 1) return;
    const updated = slides
      .filter((_, i) => i !== index)
      .map((s, i) => ({ ...s, slide: i + 1 }));
    setEditedPost(prev => ({ ...prev, visual_content: updated }));
    setCurrentSlide(Math.min(currentSlide, updated.length - 1));
  };

  const copyToClipboard = (text: string, key: string) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(key);
      setTimeout(() => setCopied(null), 1500);
    });
  };

  const copyAllSlides = () => {
    const all = slides.map((s, i) => `[Slide ${i + 1}]\n${s.text}`).join('\n\n');
    copyToClipboard(all, 'all-slides');
  };

  const handleStatusChange = (status: Post['status']) => {
    setEditedPost(prev => ({ ...prev, status }));
  };

  const handleSave = () => {
    onUpdate(editedPost);
    onClose();
  };

  const campaignClass = editedPost.campaign.includes('Legal') ? 'campaign-legal' : 'campaign-tech';

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>

        {/* ── Header ── */}
        <div className="modal-header">
          <div className="modal-header-left">
            <span className={`campaign-tag ${campaignClass}`}>{editedPost.campaign}</span>
            <span className={`status-badge status-badge-${editedPost.status}`}>
              {editedPost.status === 'pending'
                ? 'Pendiente'
                : editedPost.status === 'approved'
                ? 'Aprobado'
                : 'Descartado'}
            </span>
            <span className="modal-post-id">{editedPost.id}</span>
          </div>
          <button className="modal-close" onClick={onClose} title="Cerrar">
            <X size={20} />
          </button>
        </div>

        {/* ── Body ── */}
        <div className="modal-body">

          {/* === LEFT PANEL: Preview === */}
          <div className="modal-left">

            <div className="modal-visual-preview">
              {currentSlide > 0 && (
                <button className="slide-nav slide-prev" onClick={prevSlide}>
                  <ChevronLeft size={18} />
                </button>
              )}

              <div className="modal-slide-content" style={{ padding: editedPost.images?.[currentSlide] ? 0 : '2rem', overflow: 'hidden' }}>
                {editedPost.images && editedPost.images[currentSlide] ? (
                  <img 
                    src={editedPost.images[currentSlide]} 
                    alt={`Slide ${currentSlide + 1}`} 
                    style={{ width: '100%', height: '100%', objectFit: 'contain', display: 'block' }} 
                  />
                ) : (
                  <p>{slides[currentSlide]?.text || '(sin contenido)'}</p>
                )}
              </div>

              {currentSlide < totalSlides - 1 && (
                <button className="slide-nav slide-next" onClick={nextSlide}>
                  <ChevronRight size={18} />
                </button>
              )}

              {/* Dots indicator (Instagram style) */}
              {totalSlides > 1 && (
                <div className="slide-dots">
                  {slides.map((_, i) => (
                    <button
                      key={i}
                      className={`slide-dot ${i === currentSlide ? 'active' : ''}`}
                      onClick={() => setCurrentSlide(i)}
                      title={`Slide ${i + 1}`}
                    />
                  ))}
                </div>
              )}

              {totalSlides > 1 && (
                <span className="slide-indicator">{currentSlide + 1} / {totalSlides}</span>
              )}
            </div>

            {/* Status actions */}
            <div className="modal-actions" style={{ flexWrap: 'wrap', gap: '0.5rem' }}>
              {editedPost.images && editedPost.images[currentSlide] && (
                <button 
                  className="btn btn-secondary"
                  style={{ flex: '1 0 100%' }}
                  onClick={() => {
                    const link = document.createElement('a');
                    link.href = editedPost.images![currentSlide];
                    link.download = `${editedPost.id}_slide_${currentSlide + 1}.png`;
                    link.click();
                  }}
                >
                  <Download size={14} style={{ marginRight: '6px' }} /> Descargar Imagen
                </button>
              )}
              {editedPost.status === 'discarded' ? (
                <button className="btn btn-restore" onClick={() => handleStatusChange('pending')}>
                  <RotateCcw size={14} /> Restaurar
                </button>
              ) : (
                <>
                  <button
                    className={`btn btn-approve ${editedPost.status === 'approved' ? 'btn-status-active' : ''}`}
                    onClick={() => handleStatusChange('approved')}
                  >
                    <CheckCircle size={14} /> Aprobar
                  </button>
                  <button
                    className={`btn btn-discard ${editedPost.status === 'discarded' ? 'btn-status-active' : ''}`}
                    onClick={() => handleStatusChange('discarded')}
                  >
                    <XCircle size={14} /> Descartar
                  </button>
                </>
              )}
            </div>

            {/* Type selector */}
            <div className="modal-type-row">
              <span className="modal-type-label">Tipo de post:</span>
              <select
                className="type-select"
                value={editedPost.type}
                onChange={e => setEditedPost(prev => ({ ...prev, type: e.target.value as Post['type'] }))}
              >
                <option value="image">Imagen</option>
                <option value="carousel">Carrusel</option>
                <option value="video">Video (Voz en Off)</option>
              </select>
            </div>
          </div>

          {/* === RIGHT PANEL: Editor === */}
          <div className="modal-right">

            {/* Slides / Guión */}
            <div className="modal-section">
              <div className="modal-section-header">
                <h3>Contenido Visual{editedPost.type === 'video' ? ' / Guión' : ''}</h3>
                <span className={`slide-count-badge ${totalSlides >= MAX_SLIDES ? 'slide-count-full' : ''}`}>
                  {totalSlides} / {MAX_SLIDES} slides
                </span>
              </div>

              <div className="slides-list">
                {slides.map((slide, i) => (
                  <div
                    key={i}
                    className={`slide-item ${i === currentSlide ? 'slide-item-active' : ''}`}
                    onClick={() => setCurrentSlide(i)}
                  >
                    <span className="slide-num">{i + 1}</span>
                    <textarea
                      className="slide-text-input"
                      value={slide.text}
                      onChange={e => { e.stopPropagation(); updateSlideText(i, e.target.value); }}
                      onClick={e => e.stopPropagation()}
                      placeholder={
                        editedPost.type === 'video'
                          ? 'Guión del narrador (voz en off)...'
                          : 'Texto que aparece en la imagen...'
                      }
                      rows={2}
                    />
                    {totalSlides > 1 && (
                      <button
                        className="slide-remove-btn"
                        onClick={e => { e.stopPropagation(); removeSlide(i); }}
                        title="Eliminar slide"
                      >
                        <X size={11} />
                      </button>
                    )}
                  </div>
                ))}
              </div>

              <div className="slides-actions">
                <button className="btn btn-secondary btn-sm" onClick={copyAllSlides}>
                  <Copy size={13} />
                  {copied === 'all-slides' ? '¡Copiado!' : 'Copiar todos los slides'}
                </button>
                {editedPost.type === 'carousel' && (
                  <button
                    className="btn btn-secondary btn-sm"
                    onClick={addSlide}
                    disabled={totalSlides >= MAX_SLIDES}
                    title={totalSlides >= MAX_SLIDES ? 'Máximo 10 slides (límite Instagram)' : 'Añadir slide'}
                  >
                    <Plus size={13} /> Añadir slide
                  </button>
                )}
              </div>
            </div>

            {/* Copy / Caption */}
            <div className="modal-section">
              <div className="modal-section-header">
                <h3>Copy (Caption)</h3>
                <span className={`char-counter ${isOverLimit ? 'char-counter-over' : isNearLimit ? 'char-counter-warn' : ''}`}>
                  {copyLength.toLocaleString()} / {MAX_COPY_CHARS.toLocaleString()}
                </span>
              </div>
              <textarea
                className={`copy-textarea ${isOverLimit ? 'copy-textarea-over' : ''}`}
                value={editedPost.copy || ''}
                onChange={e => setEditedPost(prev => ({ ...prev, copy: e.target.value }))}
                placeholder="Caption de Instagram: hook, cuerpo, CTA y hashtags..."
                rows={8}
              />
              <button
                className="btn btn-secondary btn-sm"
                style={{ alignSelf: 'flex-end' }}
                onClick={() => copyToClipboard(editedPost.copy || '', 'copy')}
              >
                <Copy size={13} />
                {copied === 'copy' ? '¡Copiado!' : 'Copiar Copy'}
              </button>
            </div>

            {/* Feedback */}
            <div className="modal-section">
              <div className="modal-section-header">
                <h3>Feedback para el Agente</h3>
              </div>
              <textarea
                className="copy-textarea"
                value={editedPost.feedback || ''}
                onChange={e => setEditedPost(prev => ({ ...prev, feedback: e.target.value }))}
                placeholder="¿Por qué se descarta o modifica? El agente usará esto para mejorar en la próxima iteración..."
                rows={3}
              />
            </div>

            <button className="btn btn-save" onClick={handleSave}>
              Guardar Cambios
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
