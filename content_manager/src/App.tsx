import { useState, useEffect } from 'react';
import './index.css';
import PostCard from './components/PostCard';
import PostModal from './components/PostModal';
import { Save, Trash2, LayoutGrid, Image } from 'lucide-react';
import { DragDropContext, Droppable, Draggable } from '@hello-pangea/dnd';

export type VisualContent = { slide: number; text: string };
export type Post = {
  id: string;
  status: 'pending' | 'approved' | 'discarded';
  type: 'image' | 'carousel' | 'video';
  campaign: string;
  visual_content: VisualContent[];
  copy: string;
  feedback: string;
  images?: string[];
};

function App() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [view, setView] = useState<'board' | 'trash' | 'visuals'>('board');
  const [selectedPost, setSelectedPost] = useState<Post | null>(null);

  useEffect(() => {
    fetch('http://localhost:3001/api/posts')
      .then(res => res.json())
      .then(data => {
        setPosts(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error loading posts:', err);
        setLoading(false);
      });
  }, []);

  const handleUpdatePost = (updatedPost: Post) => {
    setPosts(prev => prev.map(p => p.id === updatedPost.id ? updatedPost : p));
  };

  const handleSaveMemory = async () => {
    setSaving(true);
    try {
      await fetch('http://localhost:3001/api/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(posts),
      });
    } catch (err) {
      alert('Error guardando memoria.');
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  const visiblePosts = posts.filter(p => {
    if (view === 'trash') return p.status === 'discarded';
    if (view === 'visuals') return p.images && p.images.length > 0;
    return p.status !== 'discarded';
  });

  const onDragEnd = (result: any) => {
    if (!result.destination || view === 'trash') return;

    const copiedVisible = Array.from(visiblePosts);
    const [movedItem] = copiedVisible.splice(result.source.index, 1);
    copiedVisible.splice(result.destination.index, 0, movedItem);

    const discarded = posts.filter(p => p.status === 'discarded');
    setPosts([...copiedVisible, ...discarded]);
  };

  if (loading) {
    return <div className="app-container"><h2>Cargando Memoria...</h2></div>;
  }

  return (
    <div className="app-container">
      <header className="header">
        <div>
          <h1 className="title">SIDMA Content Manager</h1>
          <p style={{ color: 'var(--text-secondary)' }}>
            Total posts en memoria: {posts.length} • {view === 'board' ? 'Tablero Principal' : view === 'trash' ? 'Papelera' : 'Galería Visual'}
          </p>
        </div>
        <div className="header-actions">
          <button
            className="btn btn-icon"
            onClick={() => setView(view === 'visuals' ? 'board' : 'visuals')}
            title={view === 'visuals' ? 'Volver al Tablero' : 'Ver Galería Visual'}
            style={{ color: view === 'visuals' ? 'var(--primary-color)' : '' }}
          >
            <Image size={24} />
          </button>
          <button
            className="btn btn-icon"
            onClick={() => setView(view === 'trash' ? 'board' : 'trash')}
            title={view === 'trash' ? 'Volver al Tablero' : 'Ver Descartados'}
            style={{ color: view === 'trash' ? 'var(--alert-color)' : '' }}
          >
            {view === 'trash' ? <LayoutGrid size={24} /> : <Trash2 size={24} />}
          </button>
          <button
            className="btn btn-icon"
            onClick={handleSaveMemory}
            disabled={saving}
            title="Guardar Memoria"
          >
            <Save size={24} />
          </button>
        </div>
      </header>

      {visiblePosts.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '4rem' }}>
          <h2 style={{ color: 'var(--text-secondary)' }}>
            {view === 'trash' ? 'No hay posts descartados' : view === 'visuals' ? 'No hay renders visuales generados' : 'No hay contenido en el tablero'}
          </h2>
        </div>
      ) : (
        <DragDropContext onDragEnd={onDragEnd}>
          {/* direction omitted → defaults to "vertical", which works correctly with CSS grid */}
          <Droppable droppableId="board" isDropDisabled={view === 'trash' || view === 'visuals'}>
            {(provided) => (
              <div
                className="grid"
                {...provided.droppableProps}
                ref={provided.innerRef}
              >
                {visiblePosts.map((post, index) => (
                  <Draggable
                    key={post.id}
                    draggableId={post.id}
                    index={index}
                    isDragDisabled={view === 'trash' || view === 'visuals'}
                  >
                    {(provided, snapshot) => (
                      <PostCard
                        post={post}
                        isVisualView={view === 'visuals'}
                        onUpdate={handleUpdatePost}
                        onOpenModal={() => setSelectedPost(post)}
                        innerRef={provided.innerRef}
                        draggableProps={provided.draggableProps}
                        dragHandleProps={provided.dragHandleProps}
                        isDragging={snapshot.isDragging}
                      />
                    )}
                  </Draggable>
                ))}
                {provided.placeholder}
              </div>
            )}
          </Droppable>
        </DragDropContext>
      )}

      {selectedPost && (
        <PostModal
          post={selectedPost}
          onUpdate={handleUpdatePost}
          onClose={() => setSelectedPost(null)}
        />
      )}
    </div>
  );
}

export default App;
