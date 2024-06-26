<script>
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
	<img style:--top="{a}px" src="/site/parallax/parallax0.png" alt="parallax0" />
	<img style:--top="{b}px" src="/site/parallax/parallax1.png" alt="parallax1" />
	<img style:--top="{c}px" src="/site/parallax/parallax2.png" alt="parallax2" />
	<img style:--top="{d}px" src="/site/parallax/parallax3.png" alt="parallax3" />
	<img style:--top="{e}px" src="/site/parallax/parallax4.png" alt="parallax4" />
	<img style:--top="{f}px" src="/site/parallax/parallax5.png" alt="parallax5" />
	<img style:--top="{g}px" src="/site/parallax/parallax6.png" alt="parallax6" />
	<img style:--top="{h}px" src="/site/parallax/parallax7.png" alt="parallax7" />
</section>

<svelte:window bind:scrollY />

<style>
	section {
		position: relative;
		height: calc(100vh - var(--headerHeight));
		min-height: 800px;

		background-color: #ffaf1b;
		background-color: #6CBCFF;

		mask-image: url('/site/parallax/parallax8.png');
		mask-repeat: no-repeat;
		mask-size: cover;
		mask-position: center;
		-webkit-mask-image: url('/site/parallax/parallax8.png');
		-webkit-mask-repeat: no-repeat;
		-webkit-mask-size: cover;
		-webkit-mask-position: center;
	}
	img {
		position: absolute;

		height: 100%;
		width: 100%;
		object-fit: cover;
		transform: translateY(var(--top));
		filter: hue-rotate(180deg);
	}
</style>
