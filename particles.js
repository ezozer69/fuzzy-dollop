/**
 * Particle Animation System
 * Creates dynamic particles that follow mouse movement with interactive graphics
 */

class ParticleSystem {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.particles = [];
        this.mouse = { x: 0, y: 0 };
        this.maxParticles = 50;
        this.animationId = null;
        
        this.setupCanvas();
        this.bindEvents();
        this.createInitialParticles();
        this.animate();
    }
    
    setupCanvas() {
        this.resizeCanvas();
        window.addEventListener('resize', () => this.resizeCanvas());
    }
    
    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    bindEvents() {
        document.addEventListener('mousemove', (e) => {
            this.mouse.x = e.clientX;
            this.mouse.y = e.clientY;
            
            // Create new particles at mouse position
            if (this.particles.length < this.maxParticles) {
                this.createParticle(this.mouse.x, this.mouse.y);
            }
        });
        
        document.addEventListener('click', (e) => {
            // Create burst of particles on click
            for (let i = 0; i < 10; i++) {
                this.createParticle(
                    e.clientX + (Math.random() - 0.5) * 50,
                    e.clientY + (Math.random() - 0.5) * 50
                );
            }
        });
    }
    
    createInitialParticles() {
        for (let i = 0; i < 20; i++) {
            this.createParticle(
                Math.random() * this.canvas.width,
                Math.random() * this.canvas.height
            );
        }
    }
    
    createParticle(x, y) {
        const particle = {
            x: x,
            y: y,
            vx: (Math.random() - 0.5) * 2,
            vy: (Math.random() - 0.5) * 2,
            size: Math.random() * 3 + 1,
            life: 1.0,
            decay: Math.random() * 0.02 + 0.005,
            color: {
                r: Math.floor(Math.random() * 100) + 155,
                g: Math.floor(Math.random() * 100) + 155,
                b: Math.floor(Math.random() * 255)
            },
            trail: []
        };
        
        this.particles.push(particle);
        
        // Remove oldest particles if we exceed maximum
        if (this.particles.length > this.maxParticles) {
            this.particles.shift();
        }
    }
    
    updateParticles() {
        for (let i = this.particles.length - 1; i >= 0; i--) {
            const particle = this.particles[i];
            
            // Add current position to trail
            particle.trail.push({ x: particle.x, y: particle.y });
            if (particle.trail.length > 10) {
                particle.trail.shift();
            }
            
            // Calculate attraction to mouse
            const dx = this.mouse.x - particle.x;
            const dy = this.mouse.y - particle.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < 200) {
                const force = (200 - distance) / 200 * 0.5;
                particle.vx += (dx / distance) * force * 0.1;
                particle.vy += (dy / distance) * force * 0.1;
            }
            
            // Apply some randomness
            particle.vx += (Math.random() - 0.5) * 0.1;
            particle.vy += (Math.random() - 0.5) * 0.1;
            
            // Apply damping
            particle.vx *= 0.98;
            particle.vy *= 0.98;
            
            // Update position
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            // Bounce off edges
            if (particle.x < 0 || particle.x > this.canvas.width) {
                particle.vx *= -0.8;
                particle.x = Math.max(0, Math.min(this.canvas.width, particle.x));
            }
            if (particle.y < 0 || particle.y > this.canvas.height) {
                particle.vy *= -0.8;
                particle.y = Math.max(0, Math.min(this.canvas.height, particle.y));
            }
            
            // Update life
            particle.life -= particle.decay;
            
            // Remove dead particles
            if (particle.life <= 0) {
                this.particles.splice(i, 1);
            }
        }
    }
    
    drawParticles() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw connections between nearby particles
        this.drawConnections();
        
        // Draw particle trails
        this.drawTrails();
        
        // Draw particles
        this.particles.forEach(particle => {
            const alpha = particle.life;
            
            // Draw glow effect
            this.ctx.save();
            this.ctx.globalCompositeOperation = 'lighter';
            
            // Outer glow
            const gradient = this.ctx.createRadialGradient(
                particle.x, particle.y, 0,
                particle.x, particle.y, particle.size * 3
            );
            gradient.addColorStop(0, `rgba(${particle.color.r}, ${particle.color.g}, ${particle.color.b}, ${alpha * 0.8})`);
            gradient.addColorStop(1, `rgba(${particle.color.r}, ${particle.color.g}, ${particle.color.b}, 0)`);
            
            this.ctx.fillStyle = gradient;
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size * 3, 0, Math.PI * 2);
            this.ctx.fill();
            
            // Inner particle
            this.ctx.fillStyle = `rgba(${particle.color.r}, ${particle.color.g}, ${particle.color.b}, ${alpha})`;
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            this.ctx.fill();
            
            this.ctx.restore();
        });
        
        // Draw mouse indicator
        this.drawMouseIndicator();
    }
    
    drawConnections() {
        this.ctx.save();
        this.ctx.globalCompositeOperation = 'lighter';
        
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const p1 = this.particles[i];
                const p2 = this.particles[j];
                
                const dx = p1.x - p2.x;
                const dy = p1.y - p2.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 100) {
                    const alpha = (100 - distance) / 100 * 0.3 * Math.min(p1.life, p2.life);
                    
                    this.ctx.strokeStyle = `rgba(255, 255, 255, ${alpha})`;
                    this.ctx.lineWidth = 1;
                    this.ctx.beginPath();
                    this.ctx.moveTo(p1.x, p1.y);
                    this.ctx.lineTo(p2.x, p2.y);
                    this.ctx.stroke();
                }
            }
        }
        
        this.ctx.restore();
    }
    
    drawTrails() {
        this.particles.forEach(particle => {
            if (particle.trail.length > 1) {
                this.ctx.save();
                this.ctx.globalCompositeOperation = 'lighter';
                
                for (let i = 0; i < particle.trail.length - 1; i++) {
                    const alpha = (i / particle.trail.length) * particle.life * 0.3;
                    const size = (i / particle.trail.length) * particle.size;
                    
                    this.ctx.fillStyle = `rgba(${particle.color.r}, ${particle.color.g}, ${particle.color.b}, ${alpha})`;
                    this.ctx.beginPath();
                    this.ctx.arc(particle.trail[i].x, particle.trail[i].y, size, 0, Math.PI * 2);
                    this.ctx.fill();
                }
                
                this.ctx.restore();
            }
        });
    }
    
    drawMouseIndicator() {
        if (this.mouse.x > 0 && this.mouse.y > 0) {
            this.ctx.save();
            this.ctx.globalCompositeOperation = 'lighter';
            
            const time = Date.now() * 0.005;
            const radius = 20 + Math.sin(time) * 5;
            
            // Pulsing ring around mouse
            this.ctx.strokeStyle = `rgba(255, 255, 255, 0.5)`;
            this.ctx.lineWidth = 2;
            this.ctx.beginPath();
            this.ctx.arc(this.mouse.x, this.mouse.y, radius, 0, Math.PI * 2);
            this.ctx.stroke();
            
            // Inner dot
            this.ctx.fillStyle = `rgba(255, 255, 255, 0.8)`;
            this.ctx.beginPath();
            this.ctx.arc(this.mouse.x, this.mouse.y, 2, 0, Math.PI * 2);
            this.ctx.fill();
            
            this.ctx.restore();
        }
    }
    
    animate() {
        this.updateParticles();
        this.drawParticles();
        this.animationId = requestAnimationFrame(() => this.animate());
    }
    
    destroy() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        window.removeEventListener('resize', this.resizeCanvas);
    }
}

// Initialize particle system when DOM is loaded
let particleSystem = null;

function initParticles() {
    const canvas = document.getElementById('particleCanvas');
    if (canvas) {
        particleSystem = new ParticleSystem(canvas);
    }
}

function destroyParticles() {
    if (particleSystem) {
        particleSystem.destroy();
        particleSystem = null;
    }
}

// Auto-initialize when script is loaded
document.addEventListener('DOMContentLoaded', initParticles);

// Export for manual control
window.ParticleSystem = ParticleSystem;
window.initParticles = initParticles;
window.destroyParticles = destroyParticles;