<script>
	let {
		size = 40,
		name,

		photo,
		crop = false,
		empty = null,

		area_lock = false,

		children
	} = $props();

	function get_color(str) {
		let hash = 5381;
		for (let i = 0; i < str.length; i++) {
			hash = (hash << 5) + hash + str.charCodeAt(i);
		}
		let bg = Math.abs(hash) % 361;
		let fg = bg > 29 && bg < 189 ? 'black' : 'white';
		return [bg, fg];
	}

	const get_size = () => {
		let sz = [1, size, size];
		if (!photo || !area_lock || crop) return sz;
		let match = photo.match(/_(\d+)x(\d+)\./);
		if (!match) return sz;

		sz[0] = match[1] / match[2]; //aspect-ratio
		sz[1] = Math.sqrt(size * size * sz[0]); // width
		sz[2] = sz[1] / sz[0]; // height

		return sz;
	};

	let color = get_color(name);
	let dim = get_size();
	console.log(empty);

	let src = $state(empty);
	if (photo) src = photo;
	if (crop) src += `${size}`;
</script>

{#if src}
	<img
		{src}
		alt={name}
		style:aspect-ratio={dim[0]}
		style:max-width="{dim[1]}px"
		onerror={() => (src = null)}
	/>
{:else if children}
	{@render children()}
{:else}
	<div class="avatar" style:color={color[1]} style:--hue={color[0]} style:--size="{size}px">
		{name[0]}
	</div>
{/if}

<style>
	img {
		display: block;

		width: 100%;
		object-fit: cover;

		border-radius: var(--avatar-border-radius, 8px);
	}

	.avatar {
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;

		width: var(--size);
		height: var(--size);
		border-radius: var(--avatar-border-radius, 8px);
		background-color: hsl(var(--hue), 100%, 50%);
		text-transform: capitalize;
		font-size: calc(var(--size) / 3);
		font-weight: bold;
	}
</style>
