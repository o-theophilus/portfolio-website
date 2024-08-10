<script>
	import Icon from '$lib/icon.svelte';

	let scrollY;

	let a;
	let b;
	let c;
	let d;
	let e;
	let f;
	let g;
	let h;
	let mul = (num) => num * 0.82;
	$: {
		a = mul(scrollY);
		b = mul(a);
		c = mul(b);
		d = mul(c);
		e = mul(d);
		f = mul(e);
		g = mul(f);
		h = mul(g);
	}
</script>

<section>
	<img style:--top="{a}px" src="/parallax/parallax0.png" alt="parallax0" />
	<div class="block" style:--top="{a}px">
		<div class="icon">
			<Icon icon="logo" size="6" />
		</div>
		<div class="name">Theophilus Ogbolu</div>
		<div class="role">Designer & Developer</div>
	</div>
	<img style:--top="{b}px" src="/parallax/parallax1.png" alt="parallax1" />
	<img style:--top="{c}px" src="/parallax/parallax2.png" alt="parallax2" />
	<img style:--top="{d}px" src="/parallax/parallax3.png" alt="parallax3" />
	<img style:--top="{e}px" src="/parallax/parallax4.png" alt="parallax4" />
	<img style:--top="{f}px" src="/parallax/parallax5.png" alt="parallax5" />
	<img style:--top="{g}px" src="/parallax/parallax6.png" alt="parallax6" />
	<img style:--top="{h}px" src="/parallax/parallax7.png" alt="parallax7" />
</section>

<svelte:window bind:scrollY />

<style>
	section {
		position: relative;
		height: calc(100vh - var(--headerHeight));
		min-height: 800px;

		background-color: #82c6ff;

		mask-image: url('/parallax/parallax8.png');
		mask-repeat: no-repeat;
		mask-size: cover;
		mask-position: center;
		-webkit-mask-image: url('/parallax/parallax8.png');
		-webkit-mask-repeat: no-repeat;
		-webkit-mask-size: cover;
		-webkit-mask-position: center;
	}

	img,
	.block {
		position: absolute;

		height: 100%;
		width: 100%;
		object-fit: cover;
		transform: translateY(var(--top));
	}

	.block {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;

		height: 50%;
		padding: var(--sp2);

		color: var(--bg1);
		transition: color var(--trans);
	}

	.icon {
		color: var(--cl1);
	}

	.name {
		font-size: 2rem;
		font-weight: 800;
		text-align: center;
	}

	.role {
		font-size: 1.1rem;
	}
</style>
