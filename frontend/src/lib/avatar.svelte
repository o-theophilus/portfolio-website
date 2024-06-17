<script>
	let hue = Math.floor(Math.random() * (360 + 1));
	export let size = 40;
	export let name;
	export let photo;
</script>

{#if photo}
	<img
		role="presentation"
		src={photo || '/site/no_photo.png'}
		alt={name}
		onerror="this.src='/site/no_photo.png'"
		style:--size="{size}px"
	/>
{:else}
	<div
		role="presentation"
		class="avatar"
		class:light={hue > 29 && hue < 189}
		style:--hue={hue}
		style:--size="{size}px"
	>
		<span>
			{name[0]}
		</span>
	</div>
{/if}

<style>
	img,
	.avatar {
		width: var(--size);
		height: var(--size);
		border-radius: 50%;
	}

	img {
		object-fit: cover;
	}

	.avatar {
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;

		background-color: hsl(var(--hue), 100%, 50%);
		text-transform: capitalize;
		font-size: calc(var(--size) / 3);
		font-weight: bold;

		color: var(--ft1_b);
	}
	.light {
		color: var(--ft1_d);
	}
</style>
