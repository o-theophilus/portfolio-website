<script>
	import { onMount } from 'svelte';
	import { page } from '$app/state';

	import { Datetime, Avatar } from '$lib/macro';

	let { item, parent, control } = $props();

	let _this;
	onMount(() => {
		if (page.url.hash == `#${item.key}`) {
			_this.scrollIntoView({ behavior: 'smooth' });
		}
	});
</script>

<section bind:this={_this} class:parent={parent ? false : true}>
	{@render parent?.()}

	<div class="avatar_content">
		<Avatar name={item.user.name} photo={item.user.photo} --avatar-border-radius="50%" />
		<div class="content">
			<div class="line space name_date">
				<div class="name">{item.user.name}</div>
				<div class="date"><Datetime datetime={item.date_created} type="ago" /></div>
			</div>

			<div class="username">
				@{item.user.username}
			</div>

			<div class="comment">
				{item.comment}
			</div>

			{@render control?.()}
		</div>
	</div>
</section>

<style>
	section {
		margin-top: 8px;
		padding: var(--sp2);
		border-top-left-radius: var(--sp0);
		border-radius: var(--sp0);

		background-color: var(--bg1);
	}
	.parent {
		margin: unset;
		border: 2px solid var(--bg2);
		margin-bottom: 16px;
	}

	.avatar_content {
		display: flex;
		gap: 16px;
	}

	.content {
		width: 100%;
	}

	.name_date {
		gap: 0 18px;
	}

	.name {
		color: var(--ft1);
		font-size: 0.8rem;
		font-weight: 800;
	}

	.date {
		font-size: 0.7rem;
		line-height: 100%;
	}

	.username {
		font-size: 0.7rem;
	}

	.comment {
		font-size: 0.8rem;
		margin-top: 8px;
	}
</style>
