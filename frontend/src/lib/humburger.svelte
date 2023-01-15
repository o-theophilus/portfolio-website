<script>
	import { openMobileMenu, showHeader } from '$lib/store.js';
</script>

<div
	class="humburger"
	class:openMobileMenu={$openMobileMenu}
	class:hideHeader={!$showHeader}
	on:click={() => {
		$openMobileMenu = !$openMobileMenu;
	}}
	on:keypress
>
	<div class=" one" />
	<div class=" two" />
	<div class=" three" />
</div>

<style>
	.humburger {
		--buttonSize: 50px;
		--barHeight: calc(var(--buttonSize) / 10);
		--barWidth: calc(var(--buttonSize) - var(--buttonSize) / 5);
		--barPos: calc(var(--buttonSize) / 5);
		--barPos2: calc(var(--buttonSize) / 8);
		--barCenter: calc(var(--buttonSize) / 2 - var(--barHeight) / 2);

		display: flex;
		justify-content: center;
		align-items: center;

		position: absolute;
		top: 10px;
		right: var(--gap4);

		width: var(--buttonSize);
		height: var(--buttonSize);

		border-radius: var(--gap1);
		cursor: pointer;
		background-color: transparent;

		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;

		pointer-events: auto;
	}

	.humburger div {
		position: absolute;

		height: var(--barHeight);
		width: var(--barWidth);

		border-radius: calc(var(--barHeight) / 2);
		background-color: var(--light_color);

		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}

	.one {
		top: var(--barPos);
	}
	.three {
		bottom: var(--barPos);
	}

	.hideHeader {
		background-color: var(--);
	}
	.hideHeader div {
		background-color: var(--font);
	}

	.humburger:hover:not(.openMobileMenu) .one {
		top: var(--barPos2);
	}
	.humburger:hover:not(.openMobileMenu) .three {
		bottom: var(--barPos2);
	}

	.openMobileMenu .one {
		top: var(--barCenter);
	}
	.openMobileMenu .three {
		bottom: var(--barCenter);
	}
	.openMobileMenu .one,
	.openMobileMenu .three {
		transform: rotate(45deg);
	}
	.openMobileMenu .two {
		transform: rotate(-45deg);
	}
</style>
