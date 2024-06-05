<script>
	let hue = Math.floor(Math.random() * (360 + 1));
	export let size = 40;
	export let user;
	export let profile = false;
</script>

{#if user.photo}
	<img
		on:click
		role="presentation"
		src={user.photo || '/site/no_photo.png'}
		alt={user.name}
		onerror="this.src='/site/no_photo.png'"
		style:--size="{size}px"
		class:profile
	/>
{:else}
	<div
		on:click
		role="presentation"
		class="avatar"
		class:light={hue > 29 && hue < 189}
		style:--hue={hue}
		style:--size="{size}px"
		class:profile
	>
		<span>
			{user.name[0]}
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

		color: var(--ac5_);
	}
	.light {
		color: var(--ac1_);
	}

	.profile {
		outline: 8px solid var(--ac4);
		outline-offset: 2px;
	}

	img:not(.profile),
	.avatar:not(.profile) {
		outline: 2px solid var(--ac4);
		cursor: pointer;
		transition: var(--trans);
	}

	img:not(.profile):hover,
	.avatar:not(.profile):hover {
		outline-color: var(--cl1);
	}
</style>
