<script>
	import { onMount } from 'svelte';

	let items = $state([
		{ src: 'https://picsum.photos/600/400?1', alt: 'One', label: 'One', href: '#' },
		{ src: 'https://picsum.photos/600/400?2', alt: 'Two', label: 'Two', href: '#' },
		{ src: 'https://picsum.photos/600/400?3', alt: 'Three', label: 'Three', href: '#' },
		{ src: 'https://picsum.photos/600/400?4', alt: 'Four', label: 'Four', href: '#' },
		{ src: 'https://picsum.photos/600/400?5', alt: 'Five', label: 'Five', href: '#' }
	]);

	let scroller; // track element ref
	let moved = $state(false);
	let dragging = false;
	let startX = 0;
	let startScroll = 0;

	const scrollByCard = (dir) => {
		const card = scroller?.querySelector('.card');
		if (!card) return;
		const gap = parseFloat(getComputedStyle(scroller).gap || 0);
		const width = card.offsetWidth + gap;
		scroller.scrollBy({ left: dir * width, behavior: 'smooth' });
	};

	const onPointerDown = (e) => {
		scroller.setPointerCapture?.(e.pointerId);
		dragging = true;
		moved = false;
		startX = e.clientX;
		startScroll = scroller.scrollLeft;
		scroller.classList.add('grabbing', 'dragging');
		e.preventDefault();
	};

	const onPointerMove = (e) => {
		if (!dragging) return;
		const dx = e.clientX - startX;
		if (Math.abs(dx) > 3) moved = true;
		scroller.scrollLeft = startScroll - dx;
	};

	const endDrag = (e) => {
		if (!dragging) return;
		dragging = false;
		scroller.releasePointerCapture?.(e.pointerId);
		scroller.classList.remove('grabbing', 'dragging');
	};

	onMount(() => {
		window.addEventListener('pointermove', onPointerMove, { passive: true });
		window.addEventListener('pointerup', endDrag, { passive: true });
		window.addEventListener('pointercancel', endDrag, { passive: true });

		const cancelClick = (e) => {
			if (moved) e.preventDefault();
			moved = false;
		};
		scroller.addEventListener('click', cancelClick, true);

		const onWheel = (e) => {
			if (Math.abs(e.deltaX) < Math.abs(e.deltaY)) return;
			scroller.scrollLeft += e.deltaX;
		};
		scroller.addEventListener('wheel', onWheel, { passive: true });

		return () => {
			window.removeEventListener('pointermove', onPointerMove);
			window.removeEventListener('pointerup', endDrag);
			window.removeEventListener('pointercancel', endDrag);
			scroller?.removeEventListener('wheel', onWheel);
		};
	});
</script>

<div class="carousel" aria-label="Image carousel">
	<div class="track" bind:this={scroller} onpointerdown={onPointerDown}>
		{#each items as { src, alt, label, href }}
			<a class="card" {href}>
				<img {src} {alt} />
				{#if label}
					<span>{label}</span>
				{/if}
			</a>
		{/each}
	</div>

	<button class="nav prev" onclick={() => scrollByCard(-1)} aria-label="Scroll left">‹</button>
	<button class="nav next" onclick={() => scrollByCard(1)} aria-label="Scroll right">›</button>
</div>

<style>
	* {
		box-sizing: border-box;
	}

	.carousel {
		position: relative;
		--gap: 1rem;
		--card-w: clamp(260px, 40vw, 360px);
	}

	.carousel .track {
		display: grid;
		grid-auto-flow: column;
		grid-auto-columns: var(--card-w);
		gap: var(--gap);
		overflow-x: auto;
		overscroll-behavior-x: contain;
		scroll-snap-type: x mandatory;
		scroll-padding-inline: var(--gap);
		padding: 0 var(--gap);
		-webkit-overflow-scrolling: touch;
		scrollbar-width: none;
		cursor: grab;
	}
	.carousel .track::-webkit-scrollbar {
		display: none;
	}

	.carousel .card {
		display: grid;
		align-content: end;
		border-radius: 16px;
		overflow: hidden;
		aspect-ratio: 3 / 2;
		scroll-snap-align: start;
		position: relative;
		user-select: none;
		text-decoration: none;
		color: inherit;
		background: #111;
	}
	.carousel .card img {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}
	.carousel .card span {
		position: absolute;
		inset: auto 0 0 0;
		padding: 0.6rem 0.8rem;
		background: linear-gradient(transparent, rgba(0, 0, 0, 0.55));
		color: #fff;
		font-weight: 600;
	}

	/* .carousel .track.grabbing {
		cursor: grabbing;
	}
	.carousel .track.dragging {
		scroll-snap-type: none;
	} */

	.carousel .nav {
		position: absolute;
		top: 50%;
		translate: 0 -50%;
		inline-size: 2.5rem;
		block-size: 2.5rem;
		border: none;
		border-radius: 999px;
		background: rgba(0, 0, 0, 0.6);
		color: #fff;
		font-size: 1.25rem;
		display: grid;
		place-items: center;
		cursor: pointer;
		backdrop-filter: blur(4px);
	}
	.carousel .prev {
		left: 0.5rem;
	}
	.carousel .next {
		right: 0.5rem;
	}
	.carousel .nav:focus-visible {
		outline: 2px solid #fff;
		outline-offset: 2px;
	}
</style>
