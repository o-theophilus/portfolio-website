<script>
	import { state } from '$lib/store.js';

	import Datetime from '$lib/datetime.svelte';
	import Icon from '$lib/icon.svelte';

	export let post;

	const click = () => {
		let sn = 'post_item';
		let i = $state.findIndex((x) => x.name == sn);
		if (i == -1) {
			$state.push({
				name: sn,
				data: post
			});
		} else {
			$state[i].data = post;
		}
	};
</script>

<a href="/{post.slug}" data-sveltekit-preload-data on:click={click} on:mouseenter={click}>
	<div>
		<div class="img">
			<img src={post.photos[0] || '/no_photo.png'} alt={post.title} />
		</div>
		<div class="ititle">
			<strong>
				{post.title}
			</strong>
		</div>
		<div class="description">
			{post.description}
		</div>
	</div>

	<div class="date line">
		<Datetime datetime={post.date} type="ago" />
		<div class="line info">
			<div class="line">
				<Icon icon="visibility" size="1.4" />
				{post.view}
			</div>
			<div class="line">
				<Icon icon="thumb_up" size="1.4" />
				{post._like}
			</div>
			<div class="line">
				<Icon icon="comment" size="1.4" />
				{post.comment}
			</div>
			{#if post.rating > 0}
				<div class="line">
					<Icon icon="hotel_class" size="1.4" />
					{parseFloat(post.rating)}
				</div>
			{/if}
		</div>
	</div>
</a>

<style>
	a {
		display: flex;
		flex-direction: column;
		justify-content: space-between;

		padding: var(--sp3);
		height: 100%;

		background-color: var(--bg1);
		color: var(--ft2);
		text-decoration: none;

		border-radius: var(--sp1);
		border: 2px solid transparent;

		transition: background-color var(--trans), border-color var(--trans);
	}
	a:hover {
		border-color: var(--ft2);
	}

	.img {
		border-radius: var(--sp1);
		overflow: hidden;
	}
	img {
		display: block;

		width: 100%;
		object-fit: cover;
		aspect-ratio: 1 / 1;
		background-color: var(--bg2);

		transition: transform var(--aTime);
		transition-timing-function: ease-in-out;
	}
	a:hover img {
		transform: scale(1.2) rotate(5deg);
	}
	.ititle {
		color: var(--ft1);
		margin: var(--sp2) 0;
	}

	.description {
		margin: var(--sp2) 0;
		color: var(--ft1);
		transition: color var(--trans);
	}

	.line {
		display: flex;
		align-items: center;
		gap: var(--sp0);
	}

	.date {
		font-size: 0.8rem;
		transition: color var(--trans);
		justify-content: space-between;
		flex-wrap: wrap;
		gap: var(--sp2);
	}

	.info {
		gap: var(--sp2);
	}
</style>
