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

	<div class="avatar_name_date">
		<Avatar name={item.user.name} photo={item.user.photo}  --avatar-border-radius="50%" />

		<div class="name_date">
			<div class="name_username">
				<div class="name">{item.user.name}</div>
				<div class="username">@{item.user.username}</div>
			</div>
			<div class="date"><Datetime datetime={item.date_created} type="ago" /></div>
		</div>
	</div>

	<div class="comment">
		{item.comment}
	</div>

	{@render control?.()}
</section>

<style>
	section {
		margin-top: 8px;
		padding: var(--sp2);
		border-radius: var(--sp0);

		background-color: var(--bg1);
	}
	.parent {
		margin: unset;
		margin-bottom: 16px;
		border: 2px solid var(--bg2);
	}

	.avatar_name_date {
		display: flex;
		align-items: center;
		gap: 16px;
	}

	.name_date {
		display: flex;
		align-items: flex-start;
		gap: 8px 16px;
		justify-content: space-between;
		flex-wrap: wrap;

		width: 100%;
	}

	.name {
		color: var(--ft1);
		font-size: 0.8rem;
		font-weight: 800;
		line-height: 100%;
		margin-bottom: 4px;
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
		margin-top: 16px;
	}
</style>
