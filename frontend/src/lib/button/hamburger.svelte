<script>
	let { open, onclick } = $props();
</script>

<button class="menu_btn" class:open {onclick}>
	<span>d</span>
	<div class="a"></div>
	<div class="b"></div>
	<div class="c"></div>
</button>

<style>
	span {
		display: none;
	}
	.menu_btn {
		--size: var(--hamburger-size, 40px);
		--sw: 2px;
		--sh: 20px;
		--offset: 6px;

		--mid: calc((var(--size) - var(--sw)) / 2);

		position: relative;

		display: flex;
		align-items: center;
		justify-content: center;

		width: var(--size);
		height: var(--size);
		border: none;
		border-radius: 4px;

		background-color: var(--hamburger-background-color, hsl(0, 0%, 20%));
		outline: 2px solid var(--hamburger-outline-color, transparent);
		outline-offset: -2px;
		cursor: pointer;

		transition:
			background-color 0.2s ease-in-out,
			outline-color 0.2s ease-in-out;
	}

	.menu_btn:hover {
		background-color: var(--hamburger-background-color-hover, hsl(0, 0%, 0%));
		outline: 2px solid var(--hamburger-outline-color-hover, transparent);
	}

	.menu_btn div {
		position: absolute;

		width: var(--sh);
		height: var(--sw);
		border-radius: 100px;
		top: var(--mid);

		background-color: var(--hamburger-color, hsl(0, 0%, 80%));

		transition:
			background-color 0.2s ease-in-out,
			transform 0.2s ease-in-out;
	}

	.menu_btn:hover div {
		background-color: var(--hamburger-color-hover, hsl(0, 0%, 100%));
	}

	.a {
		transform: translateY(calc(var(--offset) * -1));
	}

	.c {
		transform: translateY(var(--offset));
	}

	.open div {
		transform: translateY(0);
	}

	.open .a {
		transform: rotate(45deg);
	}

	.open .b {
		transform: rotate(-45deg);
	}

	.open .c {
		transform: rotate(45deg);
	}
</style>
